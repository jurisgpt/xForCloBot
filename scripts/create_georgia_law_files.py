#!/usr/bin/env python3

"""
Georgia Code File Creator

Creates blank markdown files for specific Georgia foreclosure law sections.
Run this script from the command line to populate the `georgia_codes` folder.
"""

import os
from pathlib import Path

# Path to target directory (update if needed)
BASE_DIR = Path.home() / "github" / "xForCloBot" / "georgia_codes"

# Filenames to be created
FILES = [
    "44-14-162.2_Notice_Requirements.md",
    "44-14-162_Advertisement_Requirements.md",
    "44-14-160_Filing_Requirements.md",
    "44-14-161_Confirmation_Requirements.md",
    "23-2-114_Powers_of_Sale.md"
]

def create_files():
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    for filename in FILES:
        file_path = BASE_DIR / filename
        if not file_path.exists():
            file_path.write_text(f"# {filename.replace('_', ' ').replace('.md', '')}\n\n> TODO: Add legal content here.")
            print(f"✅ Created: {file_path}")
        else:
            print(f"⚠️ Already exists: {file_path}")

if __name__ == "__main__":
    create_files()

