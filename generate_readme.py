#!/usr/bin/env python3
"""
Generate a comprehensive README.md from the OpenAPI specification using Redocly CLI.
"""

import json
import subprocess
import sys
import re

def run_redocly_stats() -> dict:
    """Run Redocly stats command and return JSON output."""
    try:
        result = subprocess.run(
            ['npx', '@redocly/cli', 'stats', 'api/openapi.yaml', '--format', 'json'],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running Redocly stats: {e}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error parsing Redocly stats JSON: {e}")
        return {}

def extract_basic_info() -> dict:
    """Extract basic information from the OpenAPI spec file."""
    try:
        with open('api/openapi.yaml', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract basic info using regex (simple approach)
        info = {}
        
        # Extract title
        title_match = re.search(r'title:\s*(.+)', content)
        if title_match:
            info['title'] = title_match.group(1).strip()
        
        # Extract description
        desc_match = re.search(r'description:\s*(.+)', content)
        if desc_match:
            info['description'] = desc_match.group(1).strip()
        
        # Extract version
        version_match = re.search(r'version:\s*(.+)', content)
        if version_match:
            info['version'] = version_match.group(1).strip()
        
        # Extract server URL
        server_match = re.search(r'url:\s*(.+)', content)
        if server_match:
            info['server_url'] = server_match.group(1).strip()
        
        return info
    except Exception as e:
        print(f"Error extracting basic info: {e}")
        return {}

def extract_tags() -> list:
    """Extract tags from the OpenAPI spec."""
    try:
        with open('api/openapi.yaml', 'r', encoding='utf-8') as f:
            content = f.read()
        
        tags = []
        
        # Find the tags section
        tags_section = re.search(r'tags:\s*\n((?:\s*- name:.*\n(?:\s*description:.*\n)?)+)', content, re.MULTILINE)
        if tags_section:
            tags_content = tags_section.group(1)
            
            # Extract individual tags
            tag_matches = re.findall(r'-\s*name:\s*(.+?)(?:\s*\n\s*description:\s*(.+?))?(?=\n\s*-|\n\s*$|\Z)', tags_content, re.MULTILINE | re.DOTALL)
            
            for match in tag_matches:
                tag_name = match[0].strip()
                tag_desc = match[1].strip() if match[1] else 'No description available'
                tags.append({'name': tag_name, 'description': tag_desc})
        
        return tags
    except Exception as e:
        print(f"Error extracting tags: {e}")
        return []

def generate_readme():
    """Generate the README.md file."""
    
    # Get stats from Redocly
    stats = run_redocly_stats()
    
    # Extract basic info
    info = extract_basic_info()
    
    # Extract tags
    tags = extract_tags()
    
    # Generate README content
    readme_content = f"""# {info.get('title', 'Aha! REST API Specification')}

{info.get('description', 'API for interacting with Aha! product management platform.')}

**Version:** {info.get('version', '1.0.0')}

## Overview

This OpenAPI specification defines the REST API for the Aha! product management platform. The API provides comprehensive access to features, ideas, releases, epics, and other product management resources.

## Base URL

```
{info.get('server_url', 'https://{{subdomain}}.aha.io/api/v1')}
```

## Authentication

The API supports two authentication methods:

- **OAuth 2.0**: For web applications and integrations requiring user consent
- **Bearer Token (API Key)**: For server-to-server integrations and personal access

### Rate Limiting
- **300 requests per minute** per account
- **20 requests per second** per account

When rate limits are exceeded, the API returns a `429 Too Many Requests` response.

## API Statistics

"""
    
    # Add Redocly stats
    if stats:
        readme_content += "| Feature | Count |\n"
        readme_content += "|---------|-------|\n"
        for key, value in stats.items():
            metric_name = value.get('metric', key)
            # Clean up emojis from metric names
            metric_name = re.sub(r'[🚗📦📈👉🔗🔀🎣👷🔖]\s*', '', metric_name)
            readme_content += f"| {metric_name} | {value.get('total', 0)} |\n"
        readme_content += "\n"
    
    readme_content += "## API Tags\n\n"
    
    # Add tags section
    for tag in tags:
        tag_name = tag.get('name', 'Unknown')
        tag_desc = tag.get('description', 'No description available')
        readme_content += f"### {tag_name}\n\n"
        readme_content += f"{tag_desc}\n\n"
    
    readme_content += """## Resource Overview

The API is organized around the following main resources:

"""
    
    # Add resource overview based on tags
    for tag in tags:
        tag_name = tag.get('name', 'Unknown')
        tag_desc = tag.get('description', 'No description available')
        readme_content += f"- **{tag_name}**: {tag_desc}\n"
    
    readme_content += """

## Development

### Validation

```bash
make lint
```

### Generate README

```bash
make readme
```

### View API Statistics

```bash
make stats
```

### Build HTML Documentation

```bash
make build-docs
```

## File Structure

```
api/
├── openapi.yaml          # Main OpenAPI specification
├── paths/               # API path definitions
│   ├── comments.yaml
│   ├── competitors.yaml
│   ├── features/
│   ├── ideas/
│   ├── releases/
│   └── ...
└── schemas/             # Data model schemas
    ├── comments.yaml
    ├── competitors.yaml
    ├── features/
    ├── ideas/
    ├── releases/
    └── ...
```

## Key Features

- **Comprehensive API Coverage**: {stats.get('operations', {}).get('total', 99)} operations across {stats.get('tags', {}).get('total', 18)} resource categories
- **Modular Design**: Separate files for paths and schemas for better organization
- **Flexible Authentication**: Supports both OAuth 2.0 and Bearer token authentication
- **Consistent Error Handling**: Standardized 4XX error responses across all operations
- **Rich Documentation**: Detailed descriptions, examples, and parameter documentation

## Documentation

- **OpenAPI Specification**: `api/openapi.yaml`
- **Interactive Documentation**: Available via `make build-docs`
- **Live Documentation**: [GitHub Pages](https://cedricziel.github.io/aha-spec/)
- **API Statistics**: Available via `make stats`

---

*This README was automatically generated from the OpenAPI specification using Redocly CLI stats.*
"""
    
    # Write README file
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("README.md generated successfully!")
    if stats:
        operations_count = stats.get('operations', {}).get('total', 0)
        tags_count = stats.get('tags', {}).get('total', 0)
        print(f"Generated documentation for {operations_count} operations across {tags_count} tags")

if __name__ == "__main__":
    generate_readme()