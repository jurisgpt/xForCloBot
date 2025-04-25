#!/usr/bin/env python3

import os
import re
import logging
from pathlib import Path
from dataclasses import dataclass
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@dataclass
class LawCode:
    section: str
    title: str
    category: str
    last_updated: str
    linked_file: str
    tags: str
    related_sections: str
    status: str = "Active"

class LawTracker:
    PATTERNS = {
        'section': re.compile(r'\*\*Section\*\*:\s*\[?(O\.C\.G\.A\. § [^]\n]+)'),
        'title': re.compile(r'\*\*Title\*\*:\s*\[?([^]\n]+)'),
        'category': re.compile(r'\*\*Category\*\*:\s*\[?([^]\n]+)'),
        'last_updated': re.compile(r'\*\*Last Updated\*\*:\s*\[?([^]\n]+)'),
        'tags': re.compile(r'## 🏷️ Tags\n(`[^`]+`(?:\s*`[^`]+`)*)', re.MULTILINE),
        'related_sections': re.compile(r'## 🔗 Related Sections\n((?:- [^\n]+\n?)+)', re.MULTILINE)
    }

    def __init__(self, codes_dir: Path, output_file: Path):
        self.codes_dir = codes_dir
        self.output_file = output_file
        self.entries: list[LawCode] = []

    def extract_pattern(self, content: str, pattern_name: str) -> str:
        try:
            match = self.PATTERNS[pattern_name].search(content)
            if match:
                return match.group(1).strip('[]')
            return ""
        except Exception as e:
            logging.error(f"Error extracting {pattern_name}: {e}")
            return ""

    def process_law_file(self, file_path: Path) -> LawCode | None:
        try:
            content = file_path.read_text(encoding='utf-8')
            return LawCode(
                section=self.extract_pattern(content, 'section'),
                title=self.extract_pattern(content, 'title'),
                category=self.extract_pattern(content, 'category'),
                last_updated=self.extract_pattern(content, 'last_updated'),
                tags=self.extract_pattern(content, 'tags'),
                related_sections=self.extract_pattern(content, 'related_sections'),
                linked_file=str(file_path.relative_to(self.codes_dir.parent))
            )
        except Exception as e:
            logging.error(f"Error processing {file_path}: {e}")
            return None

    def process_codes(self) -> None:
        md_files = list(self.codes_dir.glob("*.md"))
        if not md_files:
            logging.warning(f"No markdown files found in {self.codes_dir}")
            return

        for file_path in md_files:
            if file_path.name in ['README.md'] or file_path.parent.name in ['_templates', '_metadata']:
                continue
            
            if entry := self.process_law_file(file_path):
                self.entries.append(entry)
                logging.info(f"Processed: {file_path.name}")

    def save_to_csv(self) -> None:
        try:
            df = pd.DataFrame([vars(entry) for entry in self.entries])
            df.to_csv(self.output_file, index=False)
            logging.info(f"Successfully wrote {len(self.entries)} entries to {self.output_file}")
        except Exception as e:
            logging.error(f"Failed to save CSV: {e}")

    def run(self) -> bool:
        if not self.codes_dir.exists():
            logging.error(f"Law codes directory not found: {self.codes_dir}")
            return False

        try:
            self.output_file.parent.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logging.error(f"Failed to create output directory: {e}")
            return False

        self.process_codes()
        self.save_to_csv()
        return True

def main():
    script_dir = Path(__file__).resolve().parent
    CODES_DIR = script_dir.parent / "georgia_codes"
    OUTPUT_CSV = script_dir.parent / "data" / "georgia_law_tracker.csv"

    tracker = LawTracker(CODES_DIR, OUTPUT_CSV)
    if not tracker.run():
        logging.error("Failed to complete law tracking process")
        exit(1)

if __name__ == "__main__":
    main()
