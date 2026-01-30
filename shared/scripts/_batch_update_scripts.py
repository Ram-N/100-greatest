#!/usr/bin/env python3
"""
Batch update all scripts to use book_utils for path resolution.
"""

import re
from pathlib import Path

# Scripts to update and their path detection patterns
SCRIPTS_TO_UPDATE = {
    'check_book.py': {
        'imports': True,
        'replacements': [
            (
                r"db_path = Path\(__file__\)\.parent\.parent / 'database' / args\.db",
                """# Find book root and resolve paths
    if getattr(args, 'book_root', None):
        book_root = Path(args.book_root).resolve()
    else:
        book_root = find_book_root()

    db_dir = get_book_path(book_root, 'database_dir')
    db_path = db_dir / args.db"""
            ),
            (
                r"parser\.add_argument\(\s*'--export',",
                """parser.add_argument(
        '--book-root',
        type=str,
        help='Path to book root directory (auto-detected if not provided)'
    )
    parser.add_argument(
        '--export',"""
            )
        ]
    },
    'change_status.py': {
        'imports': True,
        'replacements': [
            (
                r"db_path = Path\(__file__\)\.parent\.parent / 'database' / 'master-candidates\.csv'",
                """# Find book root
    book_root = find_book_root()
    db_dir = get_book_path(book_root, 'database_dir')
    db_path = db_dir / 'master-candidates.csv'"""
            )
        ]
    },
    'update_status.py': {
        'imports': True,
        'replacements': [
            (
                r"db_path = Path\(__file__\)\.parent\.parent / 'database' / 'master-candidates\.csv'",
                """# Find book root
    book_root = find_book_root()
    db_dir = get_book_path(book_root, 'database_dir')
    db_path = db_dir / 'master-candidates.csv'"""
            ),
            (
                r"writeups_dir = Path\(__file__\)\.parent\.parent / 'book-writeups'",
                """writeups_dir = get_book_path(book_root, 'writeups_dir')"""
            )
        ]
    },
    'organize_books.py': {
        'imports': True,
        'replacements': [
            (
                r"base_dir = Path\(__file__\)\.parent\.parent",
                """# Find book root
    book_root = find_book_root()
    base_dir = book_root"""
            )
        ]
    },
    'validate_manuscript.py': {
        'imports': True,
        'replacements': [
            (
                r"base_path = Path\('/home/ram/projects/100TravelBooks'\)",
                """# Find book root
    book_root = find_book_root()
    base_path = book_root"""
            )
        ]
    },
}


def add_imports(content: str) -> str:
    """Add book_utils import if not present."""
    if 'from book_utils import' in content:
        return content

    # Find the last import statement
    lines = content.split('\n')
    last_import_idx = -1

    for i, line in enumerate(lines):
        if line.strip().startswith(('import ', 'from ')):
            last_import_idx = i

    if last_import_idx >= 0:
        # Insert after last import
        lines.insert(last_import_idx + 1, 'from book_utils import find_book_root, load_config, get_book_path')
        return '\n'.join(lines)

    return content


def update_script(script_path: Path, config: dict) -> bool:
    """Update a single script file."""
    print(f"Updating {script_path.name}...")

    try:
        content = script_path.read_text(encoding='utf-8')
        original_content = content

        # Add imports if needed
        if config.get('imports'):
            content = add_imports(content)

        # Apply replacements
        for pattern, replacement in config.get('replacements', []):
            # Use DOTALL to match across lines
            content = re.sub(pattern, replacement, content, flags=re.MULTILINE | re.DOTALL)

        if content != original_content:
            script_path.write_text(content, encoding='utf-8')
            print(f"  ✓ Updated {script_path.name}")
            return True
        else:
            print(f"  - No changes needed for {script_path.name}")
            return False

    except Exception as e:
        print(f"  ✗ Error updating {script_path.name}: {e}")
        return False


def main():
    scripts_dir = Path(__file__).parent
    updated_count = 0

    for script_name, config in SCRIPTS_TO_UPDATE.items():
        script_path = scripts_dir / script_name

        if not script_path.exists():
            print(f"Warning: {script_name} not found")
            continue

        if update_script(script_path, config):
            updated_count += 1

    print(f"\nUpdated {updated_count} scripts")


if __name__ == '__main__':
    main()
