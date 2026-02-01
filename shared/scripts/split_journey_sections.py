#!/usr/bin/env python3
"""
Split 'The Journey' sections into 'The Author' and 'The Book' sections.

Intelligently divides combined journey sections based on content analysis.
Creates backups before making changes.

Usage:
    python3 split_journey_sections.py --dry-run    # Preview changes
    python3 split_journey_sections.py --apply      # Apply changes
"""

import os
import re
import sys
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# Add script directory to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

# Import book utilities
try:
    from book_utils import find_book_root, load_config
except ImportError as e:
    print(f"Error: Cannot import book_utils.py: {e}")
    print(f"Script directory: {script_dir}")
    print("Make sure book_utils.py is in the same directory as this script")
    sys.exit(1)


class JourneySplitter:
    """Splits 'The Journey' section into 'The Author' and 'The Book'."""

    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.content = filepath.read_text(encoding='utf-8')
        self.lines = self.content.split('\n')

    def has_journey_section(self) -> bool:
        """Check if file has 'The Journey' section."""
        pattern = r'###\s+\*\*\[\s*The Journey\s*\]\*\*'
        return re.search(pattern, self.content, re.MULTILINE) is not None

    def extract_author_name(self) -> Optional[str]:
        """Extract author name from the file."""
        # Look for author name in first 10 lines (usually in subtitle or quote attribution)
        top_lines = '\n'.join(self.lines[:10])

        # Try to match: ### *Author Name*
        match = re.search(r'###\s+\*([^*]+)\*', top_lines)
        if match:
            author_full = match.group(1).strip()
            # Extract last name
            parts = author_full.split()
            if len(parts) > 0:
                return parts[-1]  # Return last name

        return None

    def split_journey_content(self, journey_content: str, author_name: Optional[str]) -> Tuple[str, str]:
        """
        Split journey content into author and book sections.

        Uses heuristics to determine the split point:
        - First paragraph often describes the author
        - Look for biographical keywords
        - Look for transition to book description
        """
        # Split into paragraphs
        paragraphs = [p.strip() for p in journey_content.split('\n\n') if p.strip()]

        if len(paragraphs) <= 1:
            # If only one paragraph, put it all in "The Book"
            return "", journey_content

        # Heuristics for determining author vs book content
        author_keywords = [
            'was a', 'was an', 'born in', 'grew up', 'studied',
            'correspondent', 'journalist', 'writer', 'author',
            'lived', 'career', 'background', 'became'
        ]

        book_keywords = [
            'the book', 'the journey', 'traveled', 'travelled',
            'went to', 'visited', 'crossed', 'expedition',
            'miles', 'route', 'destination', 'adventure'
        ]

        # Score each paragraph
        author_paragraphs = []
        book_paragraphs = []

        for i, para in enumerate(paragraphs):
            para_lower = para.lower()

            # Check if paragraph mentions author name
            author_mentioned = author_name and author_name.lower() in para_lower

            # Count keyword matches
            author_score = sum(1 for kw in author_keywords if kw in para_lower)
            book_score = sum(1 for kw in book_keywords if kw in para_lower)

            # First paragraph is often about the author
            # Unless it strongly suggests book content
            if i == 0:
                if book_score > author_score + 1:
                    book_paragraphs.append(para)
                else:
                    author_paragraphs.append(para)
            # Subsequent paragraphs
            elif author_mentioned or author_score > book_score:
                author_paragraphs.append(para)
            else:
                book_paragraphs.append(para)

        # If no clear author content, use first paragraph
        if not author_paragraphs and book_paragraphs:
            author_paragraphs = [book_paragraphs.pop(0)]

        # Join paragraphs
        author_text = '\n\n'.join(author_paragraphs)
        book_text = '\n\n'.join(book_paragraphs)

        return author_text, book_text

    def convert(self) -> str:
        """Convert the file content, replacing The Journey with The Author and The Book."""
        # Find The Journey section
        pattern = r'(###\s+\*\*\[\s*The Journey\s*\]\*\*)'
        match = re.search(pattern, self.content, re.MULTILINE)

        if not match:
            return self.content  # No change needed

        # Extract author name
        author_name = self.extract_author_name()

        # Get content after The Journey header
        start_pos = match.end()
        remaining = self.content[start_pos:]

        # Find next section (### header)
        next_section_match = re.search(r'^(###\s+\*\*\[)', remaining, re.MULTILINE)
        if next_section_match:
            journey_content = remaining[:next_section_match.start()]
            after_journey = remaining[next_section_match.start():]
        else:
            journey_content = remaining
            after_journey = ""

        # Clean up journey content
        journey_content = journey_content.strip()

        # Split into author and book sections
        author_text, book_text = self.split_journey_content(journey_content, author_name)

        # Build new sections
        new_sections = []

        if author_text:
            new_sections.append(f"### **[ The Author ]**\n\n{author_text}")
        else:
            new_sections.append(f"### **[ The Author ]**\n\n[Author biography needed]")

        new_sections.append("---")

        if book_text:
            new_sections.append(f"### **[ The Book ]**\n\n{book_text}")
        else:
            new_sections.append(f"### **[ The Book ]**\n\n[Book description needed]")

        # Construct new content
        before_journey = self.content[:match.start()]
        new_content = before_journey.rstrip() + "\n\n" + "\n\n".join(new_sections)

        if after_journey:
            new_content += "\n\n" + after_journey

        return new_content


def process_entries(book_root: Path, config: Dict, dry_run: bool = True) -> Tuple[int, int, List[str]]:
    """
    Process all book entries and split Journey sections.

    Returns:
        (total_checked, total_converted, converted_files)
    """
    writeups_dir = book_root / config['structure']['writeups_dir']
    categories = config['categories']

    total_checked = 0
    total_converted = 0
    converted_files = []

    # Create backup directory if applying changes
    if not dry_run:
        backup_dir = book_root / 'output' / f'backups-{datetime.now().strftime("%Y%m%d-%H%M%S")}'
        backup_dir.mkdir(parents=True, exist_ok=True)
        print(f"\nCreating backups in: {backup_dir.relative_to(book_root)}\n")

    for category in categories:
        category_dir = writeups_dir / category['id']

        if not category_dir.exists():
            continue

        # Find all .md files
        md_files = sorted(category_dir.glob('*.md'))

        for md_file in md_files:
            # Skip special files
            if md_file.name in ['category_intro.md', 'honorable-mentions.md']:
                continue

            total_checked += 1

            splitter = JourneySplitter(md_file)

            if not splitter.has_journey_section():
                continue

            # Convert the content
            new_content = splitter.convert()

            if new_content != splitter.content:
                total_converted += 1
                rel_path = str(md_file.relative_to(book_root))
                converted_files.append(rel_path)

                if dry_run:
                    print(f"Would convert: {rel_path}")
                else:
                    # Create backup
                    backup_file = backup_dir / md_file.name
                    shutil.copy2(md_file, backup_file)

                    # Write new content
                    md_file.write_text(new_content, encoding='utf-8')
                    print(f"✓ Converted: {rel_path}")

    return total_checked, total_converted, converted_files


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Split "The Journey" sections into "The Author" and "The Book"',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Preview changes without modifying files
    python3 split_journey_sections.py --dry-run

    # Apply changes (creates backups)
    python3 split_journey_sections.py --apply
        """
    )
    parser.add_argument('--book-root', type=str, help='Path to book root directory')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without applying')
    parser.add_argument('--apply', action='store_true', help='Apply changes to files')

    args = parser.parse_args()

    # Require either --dry-run or --apply
    if not args.dry_run and not args.apply:
        parser.error("Must specify either --dry-run or --apply")

    if args.dry_run and args.apply:
        parser.error("Cannot specify both --dry-run and --apply")

    # Find book root
    try:
        if args.book_root:
            book_root = Path(args.book_root).resolve()
        else:
            book_root = find_book_root()

        config = load_config(book_root)

        print(f"Book: {config['book']['title']}")
        print(f"Root: {book_root}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    # Process entries
    mode = "DRY RUN" if args.dry_run else "APPLY CHANGES"
    print(f"\nMode: {mode}")
    print("="*70)

    total_checked, total_converted, converted_files = process_entries(
        book_root,
        config,
        dry_run=args.dry_run
    )

    # Print summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Total entries checked: {total_checked}")
    print(f"Entries with 'The Journey' section: {total_converted}")

    if args.dry_run:
        print(f"\nRe-run with --apply to make these changes")
        print("Backups will be created automatically")
    else:
        print(f"\n✓ Successfully converted {total_converted} entries")
        print("Original files have been backed up")

    return 0


if __name__ == '__main__':
    sys.exit(main())
