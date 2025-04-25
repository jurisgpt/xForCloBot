#!/usr/bin/env python3

import re
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)

def standardize_name(filename: str) -> str:
    """Standardize case filename to CaseName_v_DefendantName_YYYY.md format."""
    if filename == "README.md":
        return filename
        
    # Extract year if present
    year_match = re.search(r'(\d{4})', filename)
    year = year_match.group(1) if year_match else ""
    
    # Remove existing year and .md extension
    base_name = re.sub(r'_?\d{4}', '', filename.replace('.md', ''))
    
    # Split on underscores and clean parts
    parts = base_name.split('_')
    
    # Capitalize each part except 'v'
    clean_parts = []
    for part in parts:
        if part.lower() == 'v':
            clean_parts.append('v')
        else:
            # Handle special cases
            if part.upper() in ['BBT', 'PNC', 'US', 'JP', 'NA']:
                clean_parts.append(part.upper())
            elif part.lower() in ['bank', 'of', 'america']:
                clean_parts.append(part.capitalize())
            else:
                clean_parts.append(part.capitalize())
    
    # Add year if present
    if year:
        clean_parts.append(year)
    
    return f"{('_'.join(clean_parts))}.md"

def main():
    cases_dir = Path(__file__).parent.parent / "court_cases"
    
    # Get all .md files except those in _templates and _metadata
    case_files = [f for f in cases_dir.glob("*.md") 
                 if f.name != "README.md" and "_" in f.name]
    
    for file_path in case_files:
        new_name = standardize_name(file_path.name)
        if new_name != file_path.name:
            new_path = file_path.parent / new_name
            try:
                file_path.rename(new_path)
                logging.info(f"Renamed: {file_path.name} -> {new_name}")
            except Exception as e:
                logging.error(f"Failed to rename {file_path.name}: {e}")

if __name__ == "__main__":
    main()
