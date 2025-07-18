#!/usr/bin/env python3

import time
import os
import re
from urllib.parse import urljoin, urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

def sanitize_filename(filename):
    """Convert URL to a safe filename"""
    filename = filename.replace('/api/resources/', '')
    filename = re.sub(r'[^\w\-_.]', '_', filename)
    filename = re.sub(r'_+', '_', filename)
    filename = filename.strip('_')
    return filename + '.md'

def clean_debug_json(json_text):
    """Clean up debug JSON format to proper JSON"""
    try:
        # This is a complex task - for now just return None if it looks like debug format
        if re.search(r'\d+ items?', json_text) or re.search(r'(string|int|bool|NULL)', json_text):
            # This appears to be debug format, return None to indicate we couldn't clean it
            return None
        return json_text
    except Exception:
        return None

def create_driver():
    """Create a headless Chrome driver"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

    # Use webdriver-manager to automatically download and setup ChromeDriver
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

def extract_parameters_table(soup):
    """Extract parameters from table format"""
    params = []

    # Find tables with "Parameters" caption
    for table in soup.find_all('table'):
        caption = table.find('caption')
        if caption and 'Parameters' in caption.get_text():
            rows = table.find('tbody').find_all('tr') if table.find('tbody') else []
            for row in rows:
                cells = row.find_all(['th', 'td'])
                if len(cells) >= 2:
                    name_cell = cells[0]
                    desc_cell = cells[1]

                    # Extract parameter name and required status
                    name = name_cell.get_text().strip()
                    required = '*' in name or 'Required' in name
                    name = re.sub(r'[*\s]', '', name)

                    description = desc_cell.get_text().strip()

                    params.append({
                        'name': name,
                        'required': required,
                        'description': description
                    })

    return params

def extract_endpoint_info(soup):
    """Extract endpoint method and path"""
    method = None
    path = None

    # Look for code blocks with HTTP method
    for code in soup.find_all('code'):
        text = code.get_text().strip()
        if re.match(r'^(GET|POST|PUT|DELETE|PATCH)\s+/', text):
            parts = text.split()
            if len(parts) >= 2:
                method = parts[0]
                path = parts[1]
                break

    return method, path

def scrape_page_with_browser(url, docs_dir):
    """Scrape a single page with browser automation"""
    driver = create_driver()

    try:
        # Navigate to the page
        driver.get(url)

        # Wait for the page to load and JavaScript to execute
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "article"))
        )

        # Give extra time for any dynamic content to load
        time.sleep(2)

        # Get the page source after JavaScript execution
        html_source = driver.page_source
        soup = BeautifulSoup(html_source, 'html.parser')

        # Find the article element
        article = soup.find('article')
        if not article:
            return f"No article found on {url}"

        # Extract structured information
        title = article.find('h1')
        title_text = title.get_text().strip() if title else "Unknown"

        method, path = extract_endpoint_info(article)
        parameters = extract_parameters_table(article)

        # Extract examples with better handling
        examples = {
            'request': None,
            'response': None,
            'curl': None
        }

        # Find pre/code blocks and categorize them
        for pre in article.find_all('pre'):
            code_text = pre.get_text().strip()

            # CURL example
            if code_text.startswith('curl'):
                examples['curl'] = code_text

            # Request body (JSON)
            elif code_text.startswith('{') and 'request' in str(pre.previous_sibling).lower():
                examples['request'] = code_text

            # Response body (JSON)
            elif code_text.startswith('{') and 'response' in str(pre.previous_sibling).lower():
                examples['response'] = code_text

        # Look for response examples in div elements with class 'pre'
        for div in article.find_all('div', class_='pre'):
            div_text = div.get_text().strip()
            if div_text and div_text.startswith('{') and not examples['response']:
                # Check if this appears to be a response by looking at surrounding context
                prev_elements = []
                current = div.previous_sibling
                for _ in range(5):  # Check 5 previous elements
                    if current:
                        prev_elements.append(str(current))
                        current = current.previous_sibling
                    else:
                        break

                context = ' '.join(prev_elements).lower()
                if 'response' in context:
                    # Try to clean up the JSON if it has debug annotations
                    clean_json = clean_debug_json(div_text)
                    examples['response'] = clean_json if clean_json else div_text

        # Also try to find JSON in script tags or other elements
        if not examples['response']:
            # Look for JSON in script tags
            for script in article.find_all('script'):
                if script.string and 'response' in script.string.lower():
                    script_content = script.string
                    # Try to extract JSON from the script
                    json_match = re.search(r'\{.*\}', script_content, re.DOTALL)
                    if json_match:
                        examples['response'] = json_match.group(0)

        # Build markdown content
        content = f"# {title_text}\n\n"
        content += f"**Source:** {url}\n\n"

        if method and path:
            content += f"## Endpoint\n\n"
            content += f"```\n{method} {path}\n```\n\n"

        if parameters:
            content += f"## Parameters\n\n"
            content += "| Name | Required | Description |\n"
            content += "|------|----------|-------------|\n"
            for param in parameters:
                required_mark = "✓" if param['required'] else ""
                content += f"| `{param['name']}` | {required_mark} | {param['description']} |\n"
            content += "\n"

        if examples['curl']:
            content += f"## Example cURL\n\n"
            content += f"```bash\n{examples['curl']}\n```\n\n"

        if examples['request']:
            content += f"## Example Request\n\n"
            content += f"```json\n{examples['request']}\n```\n\n"

        if examples['response']:
            content += f"## Example Response\n\n"
            content += f"```json\n{examples['response']}\n```\n\n"

        # Save the file
        path_part = urlparse(url).path
        filename = sanitize_filename(path_part)
        filepath = os.path.join(docs_dir, filename)

        # Skip if file already exists
        if os.path.exists(filepath):
            return f"Skipped {filepath} (already exists)"

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        return f"Saved {filepath}"

    except Exception as e:
        return f"Error scraping {url}: {e}"
    finally:
        driver.quit()

def get_all_resource_links():
    """Get all /api/resources links from the main API page"""
    driver = create_driver()
    try:
        base_url = "https://www.aha.io/api"
        driver.get(base_url)

        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # Get page source and parse
        html_source = driver.page_source
        soup = BeautifulSoup(html_source, 'html.parser')

        # Find all links containing /api/resources
        resource_links = set()
        for link in soup.find_all('a', href=True):
            href = link['href']
            if '/api/resources/' in href:
                # Convert relative URLs to absolute
                if href.startswith('/'):
                    href = urljoin(base_url, href)
                resource_links.add(href)

        return sorted(resource_links)
    finally:
        driver.quit()

def main():
    docs_dir = "docs"
    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir)

    # Get all resource links
    print("Fetching all API resource links...")
    resource_links = get_all_resource_links()
    print(f"Found {len(resource_links)} resource links")

    # Determine number of workers based on CPU count (but limit to avoid overwhelming the server)
    max_workers = min(os.cpu_count() * 2, 8)  # Cap at 8 to be respectful
    print(f"Using {max_workers} parallel workers")

    # Process URLs in parallel
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_url = {
            executor.submit(scrape_page_with_browser, url, docs_dir): url
            for url in resource_links
        }

        # Process completed tasks
        completed = 0
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            completed += 1
            try:
                result = future.result()
                print(f"[{completed}/{len(resource_links)}] {result}")
            except Exception as exc:
                print(f"[{completed}/{len(resource_links)}] Error processing {url}: {exc}")

    print(f"\nCompleted scraping {len(resource_links)} pages!")

if __name__ == "__main__":
    main()
