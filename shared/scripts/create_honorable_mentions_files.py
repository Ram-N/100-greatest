#!/usr/bin/env python3
"""
Create honorable-mentions.md files in each category directory
"""

import csv
from pathlib import Path
from collections import defaultdict
from book_utils import find_book_root, load_config, get_book_path

# Find book root and load config
book_root = find_book_root()
config = load_config(book_root)

# Build category mapping from config
category_to_dir = {}
for cat in config['categories']:
    # Create full name from short ID and name (for matching against CSV data)
    cat_id = cat['id']
    cat_name = cat['name']

    # Map both the full roman numeral name and the plain name to the ID
    roman_numerals = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX']
    cat_number = int(cat_id.split('_')[0]) if '_' in cat_id else 0
    if 0 < cat_number <= len(roman_numerals):
        full_name = f"{roman_numerals[cat_number - 1]}. {cat_name}"
        category_to_dir[full_name] = cat_id
    category_to_dir[cat_name] = cat_id

# Get database and writeups paths
db_dir = get_book_path(book_root, 'database_dir')
writeups_dir = get_book_path(book_root, 'writeups_dir')

# Read honorable mentions
hm_path = db_dir / 'honorable-mentions.csv'
with open(hm_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    books = list(reader)

# Group by category
by_category = defaultdict(list)
for book in books:
    cat = book['Theme_Category']
    by_category[cat].append(book)

# Create one-line descriptions for each book
def create_one_liner(book):
    """Generate a compelling 20-30 word one-line description"""

    title = book['Title']
    author = book['Author']
    reason = book.get('Reason_For_Honorable_Mention', '')

    # Try to extract key elements from reason
    # This is a placeholder - we'll refine these manually
    # For now, just use a shortened version of the reason

    if len(reason) > 100:
        one_liner = reason[:97] + '...'
    else:
        one_liner = reason

    return one_liner

# Generate markdown files for each category
for category_name, category_dir in category_to_dir.items():
    books_in_cat = by_category.get(category_name, [])

    if not books_in_cat:
        print(f"No books for {category_name}")
        continue

    # Sort by title
    books_in_cat.sort(key=lambda x: x['Title'])

    # Create markdown content
    content = f"# Honorable Mentions: {category_name}\n\n"
    content += f"_{len(books_in_cat)} books that also belong in this category_\n\n"
    content += "---\n\n"

    for book in books_in_cat:
        title = book['Title']
        author = book['Author']
        region = book['Primary_Region']
        one_liner = create_one_liner(book)

        # Format: **Title**, Author (Region) — Description
        content += f"**{title}**, {author} ({region}) — {one_liner}\n\n"

    # Write to file
    file_path = writeups_dir / category_dir / 'honorable-mentions.md'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ Created {file_path} ({len(books_in_cat)} books)")

print("\n" + "="*80)
print("✅ All honorable-mentions.md files created!")
print("="*80)
print("\nNOTE: The one-line descriptions are currently using the 'Reason_For_Honorable_Mention'")
print("field. You may want to refine these to be more engaging 20-30 word descriptions.")
