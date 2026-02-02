#!/usr/bin/env python3
"""
Validate book entries against canonical schema.

Validates markdown book entries against the format defined in entry-schema.json.
Supports validating individual files, multiple files, categories, or all entries.

Usage:
    python3 validate_entries.py <file.md>                    # Single file
    python3 validate_entries.py file1.md file2.md           # Multiple files
    python3 validate_entries.py "pattern*.md"               # Glob pattern
    python3 validate_entries.py --category 1_first_routes   # By category
    python3 validate_entries.py --all                       # All entries
"""

import os
import re
import sys
import json
import argparse
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
    sys.exit(1)


class ValidationSchema:
    """Loads and provides access to validation schema."""

    def __init__(self, schema_path: Path):
        self.schema_path = schema_path
        with open(schema_path, 'r', encoding='utf-8') as f:
            self.schema = json.load(f)

    def get_required_sections(self) -> List[Dict]:
        """Get list of required sections from schema."""
        return [s for s in self.schema['structure']['sections'] if s.get('required', False)]

    def get_section_by_id(self, section_id: str) -> Optional[Dict]:
        """Get section definition by ID."""
        for section in self.schema['structure']['sections']:
            if section['id'] == section_id:
                return section
        return None

    def get_validation_rules(self) -> Dict:
        """Get validation rules."""
        return self.schema.get('validation_rules', {})

    def get_formatting_rules(self) -> Dict:
        """Get formatting rules."""
        return self.schema.get('formatting_rules', {})


class EntryValidator:
    """Validates individual book entry files against schema."""

    def __init__(self, filepath: Path, schema: ValidationSchema):
        self.filepath = filepath
        self.schema = schema
        self.content = filepath.read_text(encoding='utf-8')
        self.lines = self.content.split('\n')
        self.issues = []
        self.suggestions = []

    def validate(self) -> Tuple[List[str], List[str]]:
        """Run all validations and return (issues, suggestions)."""
        self.issues = []
        self.suggestions = []

        self._check_title_block()
        self._check_opening_quote()
        self._check_subtitle_vs_author()
        self._check_required_sections()
        self._check_alternative_sections()
        self._check_author_section()
        self._check_section_content("the_author", "The Author")
        self._check_section_content("the_book", "The Book")
        self._check_signature_line()
        self._check_further_reading()
        self._check_perfect_pairing()

        return self.issues, self.suggestions

    def _check_title_block(self):
        """Check if entry has proper title block."""
        # Look for title in first few lines
        first_lines = '\n'.join(self.lines[:10])

        # Check for title (# heading)
        if not re.search(r'^#\s+.+', first_lines, re.MULTILINE):
            self.issues.append("Missing title (should be # XX — Book Title)")
            self.suggestions.append("Add title in format: # XX — [Book Title]")

    def _check_opening_quote(self):
        """Check if there's an opening quote with proper attribution in the first 20 lines."""
        top_section = '\n'.join(self.lines[:20])

        # Look for quoted text (allowing multiple quotes, question marks, etc.)
        has_quote = (
            re.search(r'^>\s+', top_section, re.MULTILINE) or
            re.search(r'\*\*"[^"]{10,}', top_section) or  # At least 10 chars after quote starts
            re.search(r'"[^"]{10,}"', top_section)
        )

        if not has_quote:
            self.issues.append("Missing opening quote (must be in first 20 lines)")
            self.suggestions.append("Add opening quote in format: **\"Quote text\"** — *Author*")
            return

        # Check if quote has proper attribution
        # Handles: **"Quote"** — *Author* OR **"Quote" "Quote2"** — *Author*
        # Also accepts regular hyphen - or em-dash —
        quote_with_attribution = re.search(
            r'\*\*"[^*]+"\*\*\s*[—\-]\s*\*([^*]+)\*',
            top_section
        )

        if not quote_with_attribution:
            self.issues.append("Opening quote missing author attribution")
            self.suggestions.append(
                "Add author attribution to quote:\n"
                "  **\"Quote text\"** — *Author Name*\n"
                "  (Use em-dash — not hyphen -)"
            )

    def _check_subtitle_vs_author(self):
        """Check if H3 subtitle contains actual author name vs. descriptive subtitle."""
        # Look for ### *...* pattern in first 15 lines
        top_section = '\n'.join(self.lines[:15])
        subtitle_match = re.search(r'###\s+\*([^*]+)\*', top_section)

        if not subtitle_match:
            return  # No subtitle found, that's okay

        subtitle_text = subtitle_match.group(1).strip()

        # Check if subtitle looks like a descriptive phrase rather than a name
        subtitle_indicators = [
            'by ', 'through', 'across', 'journey', 'voyage', 'walk',
            'travels', 'routes', 'expedition', 'adventure', 'quest',
            'road to', 'path to', 'way to', 'into', 'among', 'with',
            'searching for', 'in search of', 'on the trail'
        ]

        subtitle_lower = subtitle_text.lower()
        if any(indicator in subtitle_lower for indicator in subtitle_indicators):
            # This looks like a subtitle, not an author name
            # Extract real author from opening quote
            quote_pattern = r'\*\*"[^"]+"\*\*\s*—\s*\*([^*]+)\*'
            quote_match = re.search(quote_pattern, top_section)

            if quote_match:
                author_from_quote = quote_match.group(1).strip()
                self.issues.append(
                    f"CRITICAL: H3 contains subtitle '{subtitle_text}' instead of author name"
                )
                self.suggestions.append(
                    f"Remove subtitle or move it elsewhere. The author name is: {author_from_quote}\n"
                    f"  Change: ### *{subtitle_text}*\n"
                    f"  To: ### *{author_from_quote}*\n"
                    f"  OR remove subtitle entirely and put author in 'The Author' heading"
                )
            else:
                self.issues.append(
                    f"CRITICAL: H3 contains subtitle '{subtitle_text}' instead of author name"
                )
                self.suggestions.append(
                    "Remove subtitle or replace with actual author name\n"
                    "  OR put author name in 'The Author' section heading"
                )

    def _check_required_sections(self):
        """Check if all required section headers are present."""
        required_sections = self.schema.get_required_sections()

        for section_def in required_sections:
            section_id = section_def['id']

            # Skip sections handled by special validators
            if section_id in ['title_block', 'destinations_or_figures']:
                continue

            section_name = self._get_section_display_name(section_def)
            if not self._find_section(section_name):
                self.issues.append(f"Missing section: {section_name}")

                # Get header format from schema
                header_format = section_def.get('header_format', f"### **[ {section_name} ]**")
                self.suggestions.append(f"Add section header: {header_format}")

    def _get_section_display_name(self, section_def: Dict) -> str:
        """Extract display name from section definition."""
        name = section_def.get('name', '')
        # For sections like "The Author", "The Book", extract base name
        if ':' in name:
            return name.split(':')[0].strip()
        return name

    def _find_section(self, section_name: str) -> Optional[re.Match]:
        """Find a section header in content (allows extra content after section name)."""
        # Allow format: ### **[ Section Name ]** or ### **[ Section Name: ... ]**
        pattern = rf'###\s+\*\*\[\s*{re.escape(section_name)}(?:\s*:|\s*\])'
        return re.search(pattern, self.content, re.MULTILINE)

    def _check_alternative_sections(self):
        """Check for Destinations Explored OR Major Figures Explored."""
        alternatives = ["Destinations Explored", "Major Figures Explored"]

        found = False
        for section in alternatives:
            if self._find_section(section):
                found = True
                break

        if not found:
            self.issues.append(f"Missing section: {' OR '.join(alternatives)}")
            self.suggestions.append(
                "Add either:\n"
                "  - ### **[ Destinations Explored ]** (for geographic travel)\n"
                "  - ### **[ Major Figures Explored ]** (for historical/biographical works)"
            )

    def _check_author_section(self):
        """Check if The Author section includes author name in the heading - REQUIRED."""
        # Look for The Author section header
        pattern = r'###\s+\*\*\[\s*The Author(?:\s*:\s*([^\]]+))?\s*\]\*\*'
        match = re.search(pattern, self.content, re.MULTILINE)

        if not match:
            return  # Section missing - will be caught by _check_required_sections

        # Check if author name is in the heading (captured group 1)
        author_in_heading = match.group(1)

        if not author_in_heading or not author_in_heading.strip():
            # CRITICAL ERROR: Author name is REQUIRED in heading
            # Try to extract author name from other sources to help with fix

            # Check opening quote for author attribution
            opening_quote_pattern = r'\*\*"[^"]+"\*\*\s*—\s*\*([^*]+)\*'
            quote_match = re.search(opening_quote_pattern, self.content)

            # Check H3 subtitle (but validate it's not a descriptive subtitle)
            subtitle_pattern = r'###\s+\*([^*]+)\*'
            subtitle_match = re.search(subtitle_pattern, self.content)

            author_found = None
            if quote_match:
                author_found = quote_match.group(1).strip()
            elif subtitle_match:
                subtitle_text = subtitle_match.group(1).strip()
                # Only use subtitle if it looks like a name (not descriptive)
                subtitle_indicators = ['by ', 'through', 'across', 'journey', 'voyage']
                if not any(ind in subtitle_text.lower() for ind in subtitle_indicators):
                    author_found = subtitle_text

            if author_found:
                self.issues.append(
                    "CRITICAL: Author name missing from 'The Author' section heading"
                )
                self.suggestions.append(
                    f"Author name MUST be in the heading:\n"
                    f"  Change: ### **[ The Author ]**\n"
                    f"  To: ### **[ The Author: {author_found} ]**\n"
                    f"  (Add birth-death years if known)"
                )
            else:
                self.issues.append(
                    "CRITICAL: Author name missing from 'The Author' section heading and cannot be found elsewhere"
                )
                self.suggestions.append(
                    "Add author name to The Author heading:\n"
                    "  ### **[ The Author: Author Name (birth–death) ]**"
                )

    def _check_section_content(self, section_id: str, section_name: str):
        """Check if a section has substantive content."""
        match = self._find_section(section_name)

        if not match:
            return  # Already flagged as missing

        # Get validation rules for this section
        rules = self.schema.get_validation_rules()
        content_min = rules.get('content_minimums', {}).get(section_id, {})

        # Extract section content
        start_pos = match.end()
        remaining = self.content[start_pos:]

        # Find next section
        next_section = re.search(r'^###\s+', remaining, re.MULTILINE)
        if next_section:
            section_content = remaining[:next_section.start()]
        else:
            section_content = remaining

        # Clean and analyze content
        section_content = section_content.strip()
        text_only = re.sub(r'[*_•\-]', '', section_content)
        text_only = re.sub(r'\s+', ' ', text_only).strip()

        # Check character minimum
        min_chars = content_min.get('characters', 50)
        if len(text_only) < min_chars:
            self.issues.append(f"Section '{section_name}' has no content or is too short")
            min_words = content_min.get('words', 100)
            self.suggestions.append(
                f"Add substantive content to '{section_name}' section "
                f"(minimum {min_words} words, ~{min_chars} characters)"
            )

    def _check_signature_line(self):
        """Check for signature line quote."""
        match = self._find_section("The Signature Line")

        if not match:
            return  # Already flagged as missing

        # Extract content
        start_pos = match.end()
        remaining = self.content[start_pos:]

        next_section = re.search(r'^###\s+', remaining, re.MULTILINE)
        if next_section:
            section_content = remaining[:next_section.start()]
        else:
            section_content = remaining

        # Check for quote
        has_quote = (
            re.search(r'^>\s+', section_content, re.MULTILINE) or
            re.search(r'"[^"]{10,}"', section_content)
        )

        if not has_quote:
            self.issues.append("The Signature Line section has no quote")
            self.suggestions.append("Add blockquote: > \"Quote from the book\"")

    def _check_further_reading(self):
        """Check Further Reading subsections."""
        match = self._find_section("Further Reading")

        if not match:
            return  # Already flagged as missing

        # Extract content
        start_pos = match.end()
        remaining = self.content[start_pos:]

        next_section = re.search(r'^###\s+', remaining, re.MULTILINE)
        if next_section:
            reading_content = remaining[:next_section.start()]
        else:
            reading_content = remaining

        # Check for "In a Similar Vein:" (required)
        if "In a Similar Vein:" not in reading_content:
            self.issues.append("Further Reading missing: 'In a Similar Vein:' subsection")
            self.suggestions.append(
                "Add to Further Reading:\n"
                "**In a Similar Vein:**\n"
                "* ***Book Title*** by Author: Description"
            )

        # Check for "By [Author]:" (optional, but should have format if present)
        if "By " in reading_content and not re.search(r'\*\*By\s+\w+:', reading_content):
            self.suggestions.append(
                "Format 'By Author:' section as: **By [Author Last Name]:**"
            )

    def _check_perfect_pairing(self):
        """Check Perfect Pairing has all required subsections."""
        match = self._find_section("The Perfect Pairing")

        if not match:
            return  # Already flagged as missing

        # Extract content
        start_pos = match.end()
        remaining = self.content[start_pos:]

        next_section = re.search(r'^###\s+', remaining, re.MULTILINE)
        if next_section:
            pairing_content = remaining[:next_section.start()]
        else:
            pairing_content = remaining

        # Check required subsections
        required = ["The Drink:", "The Soundtrack:", "The Setting:"]
        missing = []

        for subsection in required:
            if subsection not in pairing_content:
                missing.append(subsection)

        if missing:
            for item in missing:
                self.issues.append(f"Perfect Pairing missing: '{item}' subsection")

            self.suggestions.append(
                "Add to Perfect Pairing:\n" +
                "\n".join(f"* **{item}** [Description]" for item in missing)
            )


def resolve_file_paths(
    args: argparse.Namespace,
    book_root: Path,
    config: Dict
) -> List[Path]:
    """
    Resolve file paths from various input methods.

    Returns list of Path objects to validate.
    """
    files_to_validate = []
    writeups_dir = book_root / config['structure']['writeups_dir']

    # Handle --all flag
    if args.all:
        categories = config['categories']
        for category in categories:
            category_dir = writeups_dir / category['id']
            if category_dir.exists():
                for md_file in category_dir.glob('*.md'):
                    # Skip special files
                    if md_file.name not in ['category_intro.md', 'honorable-mentions.md']:
                        files_to_validate.append(md_file)
        return files_to_validate

    # Handle --category flag(s)
    if args.category:
        categories = config['categories']
        category_ids = [cat['id'] for cat in categories]

        for cat_input in args.category:
            # Support both ID and name
            matching_cat = None
            for cat in categories:
                if cat['id'] == cat_input or cat['name'] == cat_input:
                    matching_cat = cat
                    break

            if not matching_cat:
                print(f"Warning: Unknown category '{cat_input}'")
                print(f"Available categories: {', '.join(category_ids)}")
                continue

            category_dir = writeups_dir / matching_cat['id']
            if category_dir.exists():
                for md_file in category_dir.glob('*.md'):
                    if md_file.name not in ['category_intro.md', 'honorable-mentions.md']:
                        files_to_validate.append(md_file)

    # Handle file arguments (direct paths or glob patterns)
    if args.files:
        for file_pattern in args.files:
            # Check if it's a direct path
            file_path = Path(file_pattern)

            # Try relative to cwd
            if file_path.exists() and file_path.is_file():
                files_to_validate.append(file_path.resolve())
                continue

            # Try relative to book root
            book_file = book_root / file_pattern
            if book_file.exists() and book_file.is_file():
                files_to_validate.append(book_file)
                continue

            # Try as glob pattern in writeups directory
            matches = list(writeups_dir.rglob(file_pattern))
            if matches:
                for match in matches:
                    if match.is_file() and match.suffix == '.md':
                        if match.name not in ['category_intro.md', 'honorable-mentions.md']:
                            files_to_validate.append(match)
                continue

            # Try glob from cwd
            from glob import glob
            glob_matches = glob(file_pattern, recursive=True)
            if glob_matches:
                for match in glob_matches:
                    match_path = Path(match)
                    if match_path.is_file() and match_path.suffix == '.md':
                        files_to_validate.append(match_path.resolve())
                continue

            print(f"Warning: No files found matching '{file_pattern}'")

    # Remove duplicates while preserving order
    seen = set()
    unique_files = []
    for f in files_to_validate:
        if f not in seen:
            seen.add(f)
            unique_files.append(f)

    return unique_files


def validate_single_file(
    filepath: Path,
    schema: ValidationSchema,
    book_root: Path,
    output_dir: Path
) -> Tuple[List[str], List[str]]:
    """
    Validate a single file and generate detailed report.

    Returns (issues, suggestions).
    """
    print(f"\nValidating: {filepath.name}")
    print("=" * 70)

    validator = EntryValidator(filepath, schema)
    issues, suggestions = validator.validate()

    # Display results
    if not issues:
        print("✅ PASSED - No issues found!")
    else:
        print(f"❌ FAILED - {len(issues)} issue(s) found:\n")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")

    if suggestions:
        print(f"\n💡 Suggestions ({len(suggestions)}):\n")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"  {i}. {suggestion}")

    # Write detailed report to file
    report_filename = f"validation-{filepath.stem}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.txt"
    report_path = output_dir / report_filename

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write(f"VALIDATION REPORT: {filepath.name}\n")
        f.write("=" * 70 + "\n")
        f.write(f"File: {filepath.relative_to(book_root)}\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Schema: {schema.schema_path.name}\n")
        f.write("=" * 70 + "\n\n")

        if not issues:
            f.write("✅ PASSED - All validation checks passed!\n\n")
        else:
            f.write(f"❌ FAILED - {len(issues)} issue(s) found:\n\n")
            for i, issue in enumerate(issues, 1):
                f.write(f"{i}. {issue}\n")

        if suggestions:
            f.write(f"\n{'=' * 70}\n")
            f.write(f"SUGGESTIONS FOR FIXES\n")
            f.write(f"{'=' * 70}\n\n")
            for i, suggestion in enumerate(suggestions, 1):
                f.write(f"{i}. {suggestion}\n\n")

        f.write(f"\n{'=' * 70}\n")
        f.write("NEXT STEPS\n")
        f.write(f"{'=' * 70}\n\n")
        if issues:
            f.write("1. Review the issues listed above\n")
            f.write("2. Edit the book entry file to fix each issue\n")
            f.write("3. Use the suggestions as guidance\n")
            f.write("4. Re-run validation to confirm fixes\n")
        else:
            f.write("Entry is ready for assembly!\n")

    print(f"\n📄 Detailed report saved to: {report_path.relative_to(book_root)}")

    return issues, suggestions


def validate_multiple_files(
    files: List[Path],
    schema: ValidationSchema,
    book_root: Path,
    verbose: bool = False
) -> Tuple[int, int, Dict[str, List[str]]]:
    """
    Validate multiple files and generate summary report.

    Returns (total_files, files_with_issues, issues_by_file).
    """
    total_files = len(files)
    files_with_issues = 0
    issues_by_file = {}

    for filepath in files:
        if verbose:
            print(f"Validating: {filepath.relative_to(book_root)}")

        validator = EntryValidator(filepath, schema)
        issues, _ = validator.validate()

        if issues:
            files_with_issues += 1
            rel_path = str(filepath.relative_to(book_root))
            issues_by_file[rel_path] = issues

    return total_files, files_with_issues, issues_by_file


def print_summary_report(
    total: int,
    issues_count: int,
    issues_by_file: Dict[str, List[str]],
    output_dir: Optional[Path] = None,
    book_root: Optional[Path] = None
):
    """Print summary validation report for multiple files and optionally save to file."""
    # Build report content
    report_lines = []
    report_lines.append("=" * 70)
    report_lines.append("VALIDATION REPORT")
    report_lines.append("=" * 70)
    report_lines.append("")
    report_lines.append(f"Total entries validated: {total}")
    report_lines.append(f"Entries with issues: {issues_count}")
    report_lines.append(f"Entries passing validation: {total - issues_count}")

    if issues_by_file:
        report_lines.append("")
        report_lines.append("=" * 70)
        report_lines.append("ISSUES FOUND")
        report_lines.append("=" * 70)

        for filepath, issues in sorted(issues_by_file.items()):
            report_lines.append("")
            report_lines.append(f"📄 {filepath}")
            for issue in issues:
                report_lines.append(f"   ❌ {issue}")
    else:
        report_lines.append("")
        report_lines.append("✅ All entries passed validation!")

    report_lines.append("")
    report_lines.append("=" * 70)

    if issues_count > 0:
        report_lines.append("")
        report_lines.append(f"⚠️  Found {issues_count} entries with issues")
        report_lines.append("   Run validation on individual files for detailed feedback")
    else:
        report_lines.append("")
        report_lines.append("✅ All entries are ready for assembly!")

    # Print to screen
    print("\n" + "\n".join(report_lines))

    # Write to file if output_dir provided
    if output_dir and book_root:
        report_filename = f"validation-summary-{datetime.now().strftime('%Y%m%d-%H%M%S')}.txt"
        report_path = output_dir / report_filename

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(report_lines))
            f.write("\n")

        rel_path = report_path.relative_to(book_root)
        print(f"\n📄 Report saved to: {rel_path}")

    if issues_count > 0:
        return 1
    else:
        return 0


def main():
    parser = argparse.ArgumentParser(
        description='Validate book entries against canonical schema',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Single file (detailed feedback + report file)
    python3 validate_entries.py blue-nile-moorehead.md

    # Multiple files (summary report)
    python3 validate_entries.py file1.md file2.md file3.md

    # Glob pattern
    python3 validate_entries.py "*salak*.md"
    python3 validate_entries.py "1_first_routes/*.md"

    # By category
    python3 validate_entries.py --category 1_first_routes
    python3 validate_entries.py --category 2_exploration --category 3_slow_routes

    # All entries
    python3 validate_entries.py --all

    # Verbose mode
    python3 validate_entries.py --all --verbose
        """
    )

    parser.add_argument('files', nargs='*', help='File(s) or pattern(s) to validate')
    parser.add_argument('--all', action='store_true', help='Validate all book entries')
    parser.add_argument('--category', action='append', help='Validate entries in specific category (can be used multiple times)')
    parser.add_argument('--book-root', type=str, help='Path to book root directory')
    parser.add_argument('--schema', type=str, help='Path to schema JSON file')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show progress for each file')

    args = parser.parse_args()

    # Show help if no arguments provided
    if not args.all and not args.category and not args.files:
        parser.print_help()
        return 0

    # Find book root
    try:
        if args.book_root:
            book_root = Path(args.book_root).resolve()
        else:
            book_root = find_book_root()

        config = load_config(book_root)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    # Load schema
    try:
        if args.schema:
            schema_path = Path(args.schema)
        else:
            schema_path = book_root / 'layouts' / 'entry-schema.json'

        if not schema_path.exists():
            print(f"Error: Schema file not found: {schema_path}", file=sys.stderr)
            print("Make sure entry-schema.json exists in layouts/ directory", file=sys.stderr)
            return 1

        schema = ValidationSchema(schema_path)

    except Exception as e:
        print(f"Error loading schema: {e}", file=sys.stderr)
        return 1

    # Resolve files to validate
    files_to_validate = resolve_file_paths(args, book_root, config)

    if not files_to_validate:
        print("No files found to validate")
        return 1

    # Create output directory for reports
    output_dir = book_root / 'output'
    output_dir.mkdir(exist_ok=True)

    # Single file: detailed report
    if len(files_to_validate) == 1:
        issues, _ = validate_single_file(
            files_to_validate[0],
            schema,
            book_root,
            output_dir
        )
        return 1 if issues else 0

    # Multiple files: summary report
    else:
        print(f"\nValidating {len(files_to_validate)} files...")
        print(f"Book: {config['book']['title']}")
        print(f"Schema: {schema_path.name}")

        total, issues_count, issues_by_file = validate_multiple_files(
            files_to_validate,
            schema,
            book_root,
            verbose=args.verbose
        )

        exit_code = print_summary_report(
            total,
            issues_count,
            issues_by_file,
            output_dir=output_dir,
            book_root=book_root
        )
        return exit_code


if __name__ == '__main__':
    sys.exit(main())
