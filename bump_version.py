#!/usr/bin/env python3
"""
Bump the version in the OpenAPI specification.
"""

import re
import sys
from datetime import datetime


def bump_version(version_string: str, bump_type: str = "patch") -> str:
    """Bump a semantic version string."""
    # Parse version (major.minor.patch)
    match = re.match(r"(\d+)\.(\d+)\.(\d+)", version_string)
    if not match:
        raise ValueError(f"Invalid version format: {version_string}")
    
    major, minor, patch = map(int, match.groups())
    
    if bump_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif bump_type == "minor":
        minor += 1
        patch = 0
    elif bump_type == "patch":
        patch += 1
    else:
        raise ValueError(f"Invalid bump type: {bump_type}")
    
    return f"{major}.{minor}.{patch}"


def update_openapi_version(file_path: str, bump_type: str = "patch") -> tuple[str, str]:
    """Update the version in the OpenAPI specification file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find current version
        version_match = re.search(r'version:\s*([0-9]+\.[0-9]+\.[0-9]+)', content)
        if not version_match:
            raise ValueError("Could not find version in OpenAPI spec")
        
        current_version = version_match.group(1)
        new_version = bump_version(current_version, bump_type)
        
        # Replace version in file
        new_content = re.sub(
            r'(version:\s*)([0-9]+\.[0-9]+\.[0-9]+)',
            f'\\g<1>{new_version}',
            content
        )
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return current_version, new_version
    
    except Exception as e:
        print(f"Error updating version: {e}")
        return None, None


def main():
    """Main function to bump version."""
    file_path = "api/openapi.yaml"
    bump_type = sys.argv[1] if len(sys.argv) > 1 else "patch"
    
    if bump_type not in ["major", "minor", "patch"]:
        print(f"Invalid bump type: {bump_type}. Use major, minor, or patch.")
        sys.exit(1)
    
    old_version, new_version = update_openapi_version(file_path, bump_type)
    
    if old_version and new_version:
        print(f"Version bumped from {old_version} to {new_version}")
        
        # Update README with new version
        try:
            import subprocess
            subprocess.run(['python3', 'generate_readme.py'], check=True)
            print("README updated with new version")
        except Exception as e:
            print(f"Warning: Could not update README: {e}")
    else:
        print("Version bump failed")
        sys.exit(1)


if __name__ == "__main__":
    main()