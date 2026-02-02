#!/usr/bin/env python3
"""
Add Table of Contents and Index to assembled manuscript.

This script post-processes an assembled manuscript to add:
1. Table of Contents (TOC) - Using Word field codes for accurate page numbers
2. Comprehensive Index - Authors, locations, titles, and keywords

Uses hybrid field code approach:
- Inserts Word TOC and INDEX field codes
- Requires one manual step: User presses F9 in Word to update fields
- Provides professional, accurate output suitable for publishing
"""

import sys
import re
import argparse
from pathlib import Path
from datetime import datetime
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

# Import from parent directory
sys.path.insert(0, str(Path(__file__).parent.parent))
from book_utils import find_book_root, load_config, get_book_path


def find_latest_manuscript(output_dir, book_short_name):
    """
    Find the most recent manuscript file.

    Args:
        output_dir: Path to output directory
        book_short_name: Short name of the book

    Returns:
        Path to the latest manuscript file

    Raises:
        FileNotFoundError: If no manuscript found
    """
    pattern = f"{book_short_name}-manuscript-*.docx"
    files = list(output_dir.glob(pattern))

    if not files:
        raise FileNotFoundError(
            f"No manuscript found matching: {pattern}\n"
            f"Run assemble_manuscript.py first."
        )

    # Sort by modification time (most recent first)
    files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return files[0]


def find_copyright_page_index(doc):
    """
    Find the index of the copyright page paragraph.

    Args:
        doc: Document object

    Returns:
        Index of the paragraph containing copyright notice

    Raises:
        ValueError: If copyright page not found
    """
    for i, para in enumerate(doc.paragraphs):
        if 'Copyright' in para.text and '2026' in para.text:
            return i

    raise ValueError("Copyright page not found in manuscript.")


def insert_toc_field(doc, insert_after_idx):
    """
    Insert TOC field code after specified paragraph index.

    Creates a Word TOC field with:
    - Outline levels 1-3 (H1=categories, H2=books, H3=authors)
    - Hyperlinks to sections
    - Professional formatting

    Args:
        doc: Document object
        insert_after_idx: Index of paragraph to insert after
    """
    # Get parent element for insertions
    parent = doc.paragraphs[insert_after_idx]._element.getparent()
    insert_position = parent.index(doc.paragraphs[insert_after_idx]._element) + 1

    # Create TOC heading
    toc_heading_element = OxmlElement('w:p')
    pPr = OxmlElement('w:pPr')
    pStyle = OxmlElement('w:pStyle')
    pStyle.set(qn('w:val'), 'Heading1')
    pPr.append(pStyle)
    toc_heading_element.append(pPr)

    run = OxmlElement('w:r')
    text_elem = OxmlElement('w:t')
    text_elem.text = 'Table of Contents'
    run.append(text_elem)
    toc_heading_element.append(run)

    parent.insert(insert_position, toc_heading_element)
    insert_position += 1

    # Create instruction paragraph
    instruction_para = OxmlElement('w:p')
    pPr = OxmlElement('w:pPr')
    jc = OxmlElement('w:jc')
    jc.set(qn('w:val'), 'center')
    pPr.append(jc)
    instruction_para.append(pPr)

    run = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')
    italic = OxmlElement('w:i')
    sz = OxmlElement('w:sz')
    sz.set(qn('w:val'), '20')  # 10pt = 20 half-points
    rPr.append(italic)
    rPr.append(sz)
    run.append(rPr)

    text_elem = OxmlElement('w:t')
    text_elem.set(qn('xml:space'), 'preserve')
    text_elem.text = '[Right-click this section and select "Update Field" to populate with page numbers]'
    run.append(text_elem)
    instruction_para.append(run)

    parent.insert(insert_position, instruction_para)
    insert_position += 1

    # Create TOC field paragraph with placeholder text
    toc_para_element = OxmlElement('w:p')

    # Create field elements
    fldChar_begin = OxmlElement('w:fldChar')
    fldChar_begin.set(qn('w:fldCharType'), 'begin')

    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = ' TOC \\o "1-3" \\h \\z \\u '

    fldChar_separate = OxmlElement('w:fldChar')
    fldChar_separate.set(qn('w:fldCharType'), 'separate')

    fldChar_end = OxmlElement('w:fldChar')
    fldChar_end.set(qn('w:fldCharType'), 'end')

    # Create runs and append to paragraph
    run_begin = OxmlElement('w:r')
    run_begin.append(fldChar_begin)
    toc_para_element.append(run_begin)

    run_instr = OxmlElement('w:r')
    run_instr.append(instrText)
    toc_para_element.append(run_instr)

    # Add separator
    run_sep = OxmlElement('w:r')
    run_sep.append(fldChar_separate)
    toc_para_element.append(run_sep)

    # Add placeholder text
    run_placeholder = OxmlElement('w:r')
    placeholder_text = OxmlElement('w:t')
    placeholder_text.text = '[Table of Contents will appear here after updating fields]'
    run_placeholder.append(placeholder_text)
    toc_para_element.append(run_placeholder)

    run_end = OxmlElement('w:r')
    run_end.append(fldChar_end)
    toc_para_element.append(run_end)

    # Insert TOC field
    parent.insert(insert_position, toc_para_element)
    insert_position += 1

    # Add page break after TOC
    page_break_para = OxmlElement('w:p')
    run = OxmlElement('w:r')
    br = OxmlElement('w:br')
    br.set(qn('w:type'), 'page')
    run.append(br)
    page_break_para.append(run)

    parent.insert(insert_position, page_break_para)


def parse_author_name(author_text):
    """
    Convert author name to "LastName, FirstName" format.

    Args:
        author_text: Author name (e.g., "Francis Parkman" or "Francis Parkman (1823-1893)")

    Returns:
        Formatted author name (e.g., "Parkman, Francis")
    """
    # Remove birth-death years in parentheses
    name = re.sub(r'\([^)]*\)', '', author_text).strip()

    # Split into parts
    parts = name.split()

    if len(parts) == 0:
        return author_text
    elif len(parts) == 1:
        return parts[0]
    else:
        # Last word is surname
        surname = parts[-1]
        first_names = ' '.join(parts[:-1])
        return f"{surname}, {first_names}"


def extract_location(bullet_text):
    """
    Extract location name from a bullet point.

    Patterns:
    - "Location Name: Description"
    - "**Location Name:** Description"
    - "Location Name (Details): Description"

    Args:
        bullet_text: Text of the bullet point

    Returns:
        Location name or None
    """
    # Try pattern with bold markers
    match = re.match(r'^[*\s]*\*\*([^:*]+):\*\*', bullet_text)
    if match:
        return match.group(1).strip()

    # Try simple colon pattern
    match = re.match(r'^([^:]+):', bullet_text)
    if match:
        location = match.group(1).strip()
        # Remove any parenthetical info like "(Beijing)"
        location = re.sub(r'\s*\([^)]*\)$', '', location)
        return location

    return None


def extract_keywords(text):
    """
    Extract keywords from a keywords line.

    Patterns:
    - "Keywords: keyword1, keyword2, keyword3"
    - "**Keywords:** keyword1, keyword2"

    Args:
        text: Text containing keywords

    Returns:
        List of keywords
    """
    # Find text after "Keywords:" (with or without asterisks)
    match = re.search(r'Keywords:\s*(.+)', text)
    if match:
        keywords_text = match.group(1).strip()
        # Remove any surrounding asterisks/italics
        keywords_text = re.sub(r'^\*+|\*+$', '', keywords_text)
        # Split on commas and clean up
        keywords = [k.strip() for k in keywords_text.split(',') if k.strip()]
        return keywords
    return []


def extract_index_entries(doc):
    """
    Extract index entries from the document.

    Parses the assembled document to find:
    - Authors (from H3 headings and quote attributions)
    - Locations (from "Destinations Explored" bullets)
    - Titles (from H2 headings)
    - Keywords (from "The Essentials" section)

    Args:
        doc: Document object

    Returns:
        Dictionary with lists of entries and their paragraph indices
    """
    index_entries = {
        'authors': [],      # (author_name, para_index)
        'locations': [],    # (location, para_index)
        'titles': [],       # (title, para_index)
        'keywords': []      # (keyword, para_index)
    }

    current_section = None
    in_destinations = False
    in_essentials = False
    current_book_start = None
    current_book_author = None

    for i, para in enumerate(doc.paragraphs):
        style_name = para.style.name if para.style else ''
        text = para.text.strip()

        if not text:
            continue

        # Book title (H2)
        if style_name == 'Heading 2':
            # Save previous book's author if we found one
            if current_book_author and current_book_start is not None:
                index_entries['authors'].append((current_book_author, current_book_start))

            # Clean up title (remove entry number prefix)
            title = re.sub(r'^\d+\s*[—\-:]\s*', '', text)
            index_entries['titles'].append((title, i))
            # Reset section tracking when we hit a new book
            in_destinations = False
            in_essentials = False
            current_book_start = i
            current_book_author = None

        # Author name from H3 (but might be subtitle, so we'll verify with quote)
        elif style_name == 'Heading 3':
            # Only use H3 if we haven't found author from quote yet
            if not current_book_author:
                author = parse_author_name(text)
                # Check if it looks like a real name (not a subtitle)
                if not any(word in text.lower() for word in ['journey', 'through', 'across', 'voyage', 'walk', 'travels']):
                    current_book_author = author

        # Extract author from quote attribution (more reliable)
        # Pattern 1: "Quote text" — *Author Name* (with asterisks)
        # Pattern 2: "Quote text" — Author Name (without asterisks)
        elif '—' in text and ('"' in text or (current_section and 'Author' in current_section)):
            # Try with asterisks first
            match = re.search(r'—\s*\*([^*]+)\*', text)
            if match:
                author_from_quote = match.group(1).strip()
                current_book_author = parse_author_name(author_from_quote)
            else:
                # Try without asterisks (plain text after em-dash)
                match = re.search(r'—\s*([A-Z][^.\n]+?)(?:\s*$|\s*\()', text)
                if match:
                    author_from_quote = match.group(1).strip()
                    # Verify it looks like a name (not a long sentence)
                    if len(author_from_quote) < 50 and ',' not in author_from_quote[:20]:
                        current_book_author = parse_author_name(author_from_quote)

        # Section heading (H4)
        elif style_name == 'Heading 4':
            current_section = text
            if 'Destinations' in text:
                in_destinations = True
                in_essentials = False
            elif 'Essentials' in text:
                in_essentials = True
                in_destinations = False
            else:
                in_destinations = False
                in_essentials = False

        # Bullet points in sections
        elif style_name == 'List Bullet':
            # Destinations Explored section
            if in_destinations:
                location = extract_location(text)
                if location:
                    index_entries['locations'].append((location, i))

            # Keywords in Essentials section
            elif in_essentials and 'Keywords' in text:
                keywords = extract_keywords(text)
                for keyword in keywords:
                    index_entries['keywords'].append((keyword, i))

    # Don't forget the last book's author
    if current_book_author and current_book_start is not None:
        index_entries['authors'].append((current_book_author, current_book_start))

    return index_entries


def insert_xe_field(para_element, entry_text):
    """
    Insert a hidden XE (Index Entry) field after a paragraph.

    Args:
        para_element: Paragraph XML element
        entry_text: Text for the index entry
    """
    # Create XE field paragraph (hidden)
    xe_para = OxmlElement('w:p')

    # Create field elements
    fldChar_begin = OxmlElement('w:fldChar')
    fldChar_begin.set(qn('w:fldCharType'), 'begin')

    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = f' XE "{entry_text}" '

    fldChar_end = OxmlElement('w:fldChar')
    fldChar_end.set(qn('w:fldCharType'), 'end')

    # Create run with field
    run = OxmlElement('w:r')

    # Make run hidden
    rPr = OxmlElement('w:rPr')
    vanish = OxmlElement('w:vanish')
    rPr.append(vanish)
    run.append(rPr)

    run.append(fldChar_begin)

    run_instr = OxmlElement('w:r')
    run_instr.append(instrText)

    run_end = OxmlElement('w:r')
    run_end.append(fldChar_end)

    xe_para.append(run)
    xe_para.append(run_instr)
    xe_para.append(run_end)

    # Insert after the specified paragraph
    parent = para_element.getparent()
    parent.insert(parent.index(para_element) + 1, xe_para)


def insert_index_entries(doc, index_entries):
    """
    Insert hidden XE fields throughout the document.

    Args:
        doc: Document object
        index_entries: Dictionary of index entries with paragraph indices

    Returns:
        Total count of inserted entries
    """
    total_entries = 0

    # Track which paragraphs we've already processed to avoid duplicates
    # and to insert fields in reverse order (to preserve indices)
    all_entries = []

    # Collect all entries with their positions
    for author, idx in index_entries['authors']:
        all_entries.append((idx, author))

    for location, idx in index_entries['locations']:
        all_entries.append((idx, location))

    for title, idx in index_entries['titles']:
        all_entries.append((idx, title))

    for keyword, idx in index_entries['keywords']:
        all_entries.append((idx, keyword))

    # Sort by index in reverse order (so we don't mess up indices when inserting)
    all_entries.sort(key=lambda x: x[0], reverse=True)

    # Remove duplicates (same entry at same position)
    seen = set()
    unique_entries = []
    for idx, text in all_entries:
        key = (idx, text)
        if key not in seen:
            seen.add(key)
            unique_entries.append((idx, text))

    # Insert XE fields
    for idx, entry_text in unique_entries:
        if idx < len(doc.paragraphs):
            para_element = doc.paragraphs[idx]._element
            insert_xe_field(para_element, entry_text)
            total_entries += 1

    return total_entries


def insert_index_field(doc):
    """
    Insert INDEX field at the end of the document.

    Creates a Word INDEX field with:
    - Two-column layout
    - Letter headings
    - Professional formatting

    Args:
        doc: Document object
    """
    # Get the body element (parent of all paragraphs)
    body = doc._element.body

    # Create page break paragraph
    page_break_para = OxmlElement('w:p')
    run = OxmlElement('w:r')
    br = OxmlElement('w:br')
    br.set(qn('w:type'), 'page')
    run.append(br)
    page_break_para.append(run)
    body.append(page_break_para)

    # Create Index heading
    index_heading = OxmlElement('w:p')
    pPr = OxmlElement('w:pPr')
    pStyle = OxmlElement('w:pStyle')
    pStyle.set(qn('w:val'), 'Heading1')
    pPr.append(pStyle)
    index_heading.append(pPr)

    run = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')
    sz = OxmlElement('w:sz')
    sz.set(qn('w:val'), '48')  # 24pt = 48 half-points
    rPr.append(sz)
    run.append(rPr)

    text_elem = OxmlElement('w:t')
    text_elem.text = 'Index'
    run.append(text_elem)
    index_heading.append(run)
    body.append(index_heading)

    # Create instruction paragraph
    instruction_para = OxmlElement('w:p')
    pPr = OxmlElement('w:pPr')
    jc = OxmlElement('w:jc')
    jc.set(qn('w:val'), 'center')
    pPr.append(jc)
    instruction_para.append(pPr)

    run = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')
    italic = OxmlElement('w:i')
    sz = OxmlElement('w:sz')
    sz.set(qn('w:val'), '20')  # 10pt = 20 half-points
    rPr.append(italic)
    rPr.append(sz)
    run.append(rPr)

    text_elem = OxmlElement('w:t')
    text_elem.set(qn('xml:space'), 'preserve')
    text_elem.text = '[Right-click below and select "Update Field" to generate the index]'
    run.append(text_elem)
    instruction_para.append(run)
    body.append(instruction_para)

    # Create INDEX field paragraph with placeholder text
    index_para = OxmlElement('w:p')

    # Create field elements
    fldChar_begin = OxmlElement('w:fldChar')
    fldChar_begin.set(qn('w:fldCharType'), 'begin')

    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = ' INDEX \\e " " \\h "A" \\c "2" '

    fldChar_separate = OxmlElement('w:fldChar')
    fldChar_separate.set(qn('w:fldCharType'), 'separate')

    fldChar_end = OxmlElement('w:fldChar')
    fldChar_end.set(qn('w:fldCharType'), 'end')

    # Create runs and append to paragraph
    run_begin = OxmlElement('w:r')
    run_begin.append(fldChar_begin)
    index_para.append(run_begin)

    run_instr = OxmlElement('w:r')
    run_instr.append(instrText)
    index_para.append(run_instr)

    # Add separator
    run_sep = OxmlElement('w:r')
    run_sep.append(fldChar_separate)
    index_para.append(run_sep)

    # Add placeholder text
    run_placeholder = OxmlElement('w:r')
    placeholder_text = OxmlElement('w:t')
    placeholder_text.text = '[Index will appear here after updating fields]'
    run_placeholder.append(placeholder_text)
    index_para.append(run_placeholder)

    run_end = OxmlElement('w:r')
    run_end.append(fldChar_end)
    index_para.append(run_end)

    body.append(index_para)


def validate_document_structure(doc):
    """
    Validate that the document has the expected structure.

    Args:
        doc: Document object

    Raises:
        ValueError: If document structure is invalid
    """
    has_h2 = any(p.style and p.style.name == 'Heading 2' for p in doc.paragraphs)
    if not has_h2:
        raise ValueError("Invalid manuscript: No book entries (Heading 2) found.")


def check_for_existing_toc(doc):
    """
    Check if document already has a TOC.

    Args:
        doc: Document object

    Returns:
        True if TOC found, False otherwise
    """
    for para in doc.paragraphs:
        if para.text.strip() == 'Table of Contents' and para.style and 'Heading' in para.style.name:
            return True
    return False


def check_for_existing_index(doc):
    """
    Check if document already has an Index.

    Args:
        doc: Document object

    Returns:
        True if Index found, False otherwise
    """
    for para in doc.paragraphs:
        if para.text.strip() == 'Index' and para.style and 'Heading' in para.style.name:
            return True
    return False


def main():
    """Main function to add TOC and Index to manuscript."""
    parser = argparse.ArgumentParser(
        description='Add Table of Contents and Index to assembled manuscript'
    )
    parser.add_argument(
        '--book-root',
        type=str,
        help='Path to book root directory (auto-detected if not provided)'
    )
    parser.add_argument(
        '--manuscript',
        type=str,
        help='Path to manuscript file (auto-detects latest if not provided)'
    )
    parser.add_argument(
        '--toc-only',
        action='store_true',
        help='Only add Table of Contents'
    )
    parser.add_argument(
        '--index-only',
        action='store_true',
        help='Only add Index'
    )
    args = parser.parse_args()

    # Find book root and load config
    if args.book_root:
        base_path = Path(args.book_root).resolve()
    else:
        base_path = find_book_root()

    config = load_config(base_path)
    book_short_name = config['book']['short_name']
    output_dir = get_book_path(base_path, 'output_dir')

    # Find manuscript file
    if args.manuscript:
        manuscript_path = Path(args.manuscript)
    else:
        manuscript_path = find_latest_manuscript(output_dir, book_short_name)

    print(f"Processing: {manuscript_path}")

    # Load document
    doc = Document(manuscript_path)

    # Validate structure
    validate_document_structure(doc)

    # Add TOC
    if not args.index_only:
        if check_for_existing_toc(doc):
            print("\n⚠ Table of Contents already exists in document. Skipping TOC insertion.")
            print("  To regenerate, use the original manuscript without TOC.")
        else:
            print("\nInserting Table of Contents field...")
            try:
                copyright_idx = find_copyright_page_index(doc)
                insert_toc_field(doc, copyright_idx)
                print("✓ TOC field inserted after copyright page")
            except ValueError as e:
                print(f"Warning: {e}")
                print("Skipping TOC insertion")

    # Add Index
    if not args.toc_only:
        if check_for_existing_index(doc):
            print("\n⚠ Index already exists in document. Skipping Index insertion.")
            print("  To regenerate, use the original manuscript without Index.")
            return  # Exit early since we can't save without changes

        if args.index_only and check_for_existing_toc(doc):
            # If only adding index and TOC exists, we can proceed
            pass
        print("\nExtracting index entries...")
        index_entries = extract_index_entries(doc)

        total_authors = len(index_entries['authors'])
        total_locations = len(index_entries['locations'])
        total_keywords = len(index_entries['keywords'])
        total_titles = len(index_entries['titles'])

        print(f"Found {total_authors} authors, {total_locations} locations, "
              f"{total_keywords} keywords, {total_titles} titles")

        print("Inserting XE index fields...")
        total_entries = insert_index_entries(doc, index_entries)
        print(f"✓ {total_entries} index entries marked")

        print("\nInserting INDEX field at end...")
        insert_index_field(doc)
        print("✓ Index field inserted")

    # Save document
    timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M')
    filename = f"{book_short_name}-manuscript-with-toc-{timestamp}.docx"
    output_path = output_dir / filename

    doc.save(output_path)
    print(f"\n✓ Saved to: {output_path}")

    # Print instructions
    print("\n" + "="*60)
    print("Next steps:")
    print("  1. Open the document in Microsoft Word")
    print("  2. Press Ctrl+A (Select All)")
    print("  3. Press F9 (Update Fields)")
    print("  4. Save and export to PDF for publishing")
    print("="*60)


if __name__ == '__main__':
    main()
