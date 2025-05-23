#!/usr/bin/env python3
"""
Court Case Tracker Update Script

This script processes markdown files containing court case information and generates
a CSV tracker. It extracts case titles, jurisdictions, years, and other relevant
information from properly formatted markdown files.
"""

import os
import re
import logging
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass
import pandas as pd
import textwrap

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@dataclass
class CaseData:
    title: str
    jurisdiction: str
    year: str
    key_issues: str
    outcome: str
    linked_file: str
    tags: str
    status: str = "Published"
    
    @property
    def case_key(self) -> str:
        """Generate a unique key for deduplication"""
        # Remove special characters and convert to lowercase
        clean_title = ''.join(c.lower() for c in self.title if c.isalnum())
        return f"{clean_title}_{self.year}"

class CaseTracker:
    PATTERNS = {
        'title': re.compile(r"# (.+?)\s+\("),
        'year': re.compile(r"\((\d{4})\)"),
        'court': re.compile(r"\*\*Court\*\*: (.+)"),
        'tags': re.compile(r"### 🔖 Tags\n`(.+?)`", re.DOTALL),
        'key_issues': re.compile(r"### 📝 Key Issues\n(.+?)\n(?:###|$)", re.DOTALL),
        'outcome': re.compile(r"### ⚖️ Outcome\n(.+?)\n(?:###|$)", re.DOTALL)
    }

    def __init__(self, cases_dir: Path, output_file: Path):
        self.cases_dir = cases_dir
        self.output_file = output_file
        self.entries: List[CaseData] = []

    def validate_paths(self) -> bool:
        if not self.cases_dir.exists():
            logging.error(f"Court cases directory not found: {self.cases_dir}")
            return False
        try:
            self.output_file.parent.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            logging.error(f"Failed to create output directory: {e}")
            return False

    def extract_pattern(self, content: str, pattern_name: str) -> str:
        try:
            match = self.PATTERNS[pattern_name].search(content)
            if match:
                return match.group(1).strip()
        except Exception as e:
            logging.warning(f"Error extracting {pattern_name}: {e}")
        return "Unknown" if pattern_name in ['title', 'year', 'court'] else ""

    def process_case_file(self, file_path: Path) -> Optional[CaseData]:
        try:
            content = file_path.read_text(encoding='utf-8')
            return CaseData(
                title=self.extract_pattern(content, 'title'),
                jurisdiction=self.extract_pattern(content, 'court'),
                year=self.extract_pattern(content, 'year'),
                key_issues=self.extract_pattern(content, 'key_issues'),
                outcome=self.extract_pattern(content, 'outcome'),
                linked_file=str(file_path.relative_to(self.cases_dir.parent)),
                tags=self.extract_pattern(content, 'tags')
            )
        except Exception as e:
            logging.error(f"Error processing {file_path}: {e}")
            return None

    def process_cases(self) -> None:
        md_files = list(self.cases_dir.glob("*.md"))
        if not md_files:
            logging.warning(f"No markdown files found in {self.cases_dir}")
            return

        # Use dictionary for deduplication
        case_dict = {}
        
        for file_path in md_files:
            if entry := self.process_case_file(file_path):
                case_key = entry.case_key
                
                # Skip README and consolidated files
                if file_path.name in ['README.md', 'wrongful_foreclosure_cases.md']:
                    continue
                    
                # Handle duplicate case
                if case_key in case_dict:
                    existing = case_dict[case_key]
                    # Keep the entry with more information
                    if len(entry.key_issues or '') > len(existing.key_issues or ''):
                        case_dict[case_key] = entry
                else:
                    case_dict[case_key] = entry
                logging.info(f"Processed: {file_path.name}")
        
        self.entries = list(case_dict.values())

    def save_to_csv(self) -> None:
        try:
            wrapped_entries = []
            for entry in self.entries:
                entry_dict = vars(entry).copy()
                # Word wrap key_issues and outcome to 80 chars per line
                for field in ['key_issues', 'outcome']:
                    if entry_dict[field]:
                        entry_dict[field] = textwrap.fill(entry_dict[field], width=80)
                # Strip and standardize all string fields
                for k, v in entry_dict.items():
                    if isinstance(v, str):
                        entry_dict[k] = v.strip().replace('\r\n', '\n')
                wrapped_entries.append(entry_dict)
            df = pd.DataFrame(wrapped_entries)
            df.to_csv(self.output_file, index=False)
            logging.info(f"Successfully wrote {len(self.entries)} entries to {self.output_file}")
        except Exception as e:
            logging.error(f"Failed to save CSV: {e}")

    def run(self) -> bool:
        if not self.validate_paths():
            return False

        self.process_cases()
        if not self.entries:
            logging.error("No valid entries found to process")
            return False

        self.save_to_csv()
        return True

def main():
    script_dir = Path(__file__).resolve().parent
    COURT_CASES_DIR = script_dir.parent / "court_cases"
    OUTPUT_CSV = script_dir.parent / "data" / "xForCloBot_Case_Tracker.csv"

    tracker = CaseTracker(COURT_CASES_DIR, OUTPUT_CSV)
    if not tracker.run():
        logging.error("Failed to complete case tracking process")
        exit(1)

if __name__ == "__main__":
    main()
