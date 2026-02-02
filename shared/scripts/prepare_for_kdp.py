#!/usr/bin/env python3
"""
Prepare manuscript for Kindle Direct Publishing (KDP).

This script optimizes a manuscript for ebook distribution:
1. Creates/updates TOC without page numbers (ebooks don't have page numbers)
2. Adds "toc" bookmark to TOC heading (required by KDP)
3. Removes Index section (not useful in ebooks)
4. Ensures proper hyperlink navigation
5. Optimizes for Kindle reading experience

Usage:
    python3 prepare_for_kdp.py
    python3 prepare_for_kdp.py --manuscript output/manuscript.docx
"""

import sys
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
    # Try with-toc files first, then regular manuscript files
    patterns = [
        f"{book_short_name}-manuscript-with-toc-*.docx",
        f"{book_short_name}-manuscript-*.docx"
    ]

    for pattern in patterns:
        files = list(output_dir.glob(pattern))
        if files:
            files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
            return files[0]

    raise FileNotFoundError(
        f"No manuscript found in {output_dir}\n"
        f"Run assemble_manuscript.py first."
    )


def find_toc_heading(doc):
    """
    Find the Table of Contents heading paragraph.

    Args:
        doc: Document object

    Returns:
        (index, paragraph) tuple or (None, None) if not found
    """
    for i, para in enumerate(doc.paragraphs):
        if para.text.strip() == 'Table of Contents' and para.style and 'Heading' in para.style.name:
            return i, para
    return None, None


def find_index_heading(doc):
    """
    Find the Index heading paragraph.

    Args:
        doc: Document object

    Returns:
        Index of Index heading or None if not found
    """
    for i, para in enumerate(doc.paragraphs):
        if para.text.strip() == 'Index' and para.style and 'Heading' in para.style.name:
            return i
    return None


def add_bookmark(para, bookmark_name):
    """
    Add a bookmark to a paragraph.

    Args:
        para: Paragraph object
        bookmark_name: Name of the bookmark (e.g., "toc")
    """
    # Get the paragraph element
    p = para._element

    # Create bookmark start
    bookmark_start = OxmlElement('w:bookmarkStart')
    bookmark_start.set(qn('w:id'), '0')
    bookmark_start.set(qn('w:name'), bookmark_name)

    # Create bookmark end
    bookmark_end = OxmlElement('w:bookmarkEnd')
    bookmark_end.set(qn('w:id'), '0')

    # Insert at beginning and end of paragraph
    p.insert(0, bookmark_start)
    p.append(bookmark_end)


def remove_toc_page_numbers(doc, toc_idx):
    """
    Remove page numbers from existing TOC field.

    Modifies the TOC field code to remove page number display.

    Args:
        doc: Document object
        toc_idx: Index of TOC heading paragraph

    Returns:
        True if TOC field found and modified, False otherwise
    """
    # Look for TOC field in next few paragraphs
    for i in range(toc_idx, min(toc_idx + 10, len(doc.paragraphs))):
        para = doc.paragraphs[i]
        para_xml = para._element.xml.decode('utf-8') if hasattr(para._element.xml, 'decode') else str(para._element.xml)

        if 'TOC' in para_xml and 'instrText' in para_xml:
            # Found the TOC field - modify it
            for elem in para._element.iter():
                if elem.tag == qn('w:instrText'):
                    # Modify field code to remove page numbers
                    # Change: TOC \o "1-3" \h \z \u
                    # To: TOC \o "1-3" \h \n (n = no page numbers)
                    old_text = elem.text
                    if old_text and 'TOC' in old_text:
                        # Remove \z and \u switches, add \n switch
                        new_text = old_text.replace('\\z', '').replace('\\u', '').strip()
                        if '\\n' not in new_text:
                            new_text += ' \\n'
                        elem.text = new_text
                        return True
    return False


def create_kdp_toc(doc, insert_after_idx, categories_and_books):
    """
    Create a KDP-compatible TOC with hyperlinks but no page numbers.

    Args:
        doc: Document object
        insert_after_idx: Paragraph index to insert after (typically copyright page)
        categories_and_books: List of (category_name, [book_titles]) tuples
    """
    parent = doc.paragraphs[insert_after_idx]._element.getparent()
    insert_position = parent.index(doc.paragraphs[insert_after_idx]._element) + 1

    # Create TOC heading
    toc_heading = OxmlElement('w:p')
    pPr = OxmlElement('w:pPr')
    pStyle = OxmlElement('w:pStyle')
    pStyle.set(qn('w:val'), 'Heading1')
    pPr.append(pStyle)
    toc_heading.append(pPr)

    run = OxmlElement('w:r')
    text_elem = OxmlElement('w:t')
    text_elem.text = 'Table of Contents'
    run.append(text_elem)
    toc_heading.append(run)

    parent.insert(insert_position, toc_heading)
    insert_position += 1

    # Add bookmark to TOC heading
    bookmark_start = OxmlElement('w:bookmarkStart')
    bookmark_start.set(qn('w:id'), '0')
    bookmark_start.set(qn('w:name'), 'toc')
    bookmark_end = OxmlElement('w:bookmarkEnd')
    bookmark_end.set(qn('w:id'), '0')

    toc_heading.insert(0, bookmark_start)
    toc_heading.append(bookmark_end)

    # Create TOC field with \n switch (no page numbers)
    toc_field = OxmlElement('w:p')

    fldChar_begin = OxmlElement('w:fldChar')
    fldChar_begin.set(qn('w:fldCharType'), 'begin')

    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = ' TOC \\o "1-3" \\h \\n '

    fldChar_separate = OxmlElement('w:fldChar')
    fldChar_separate.set(qn('w:fldCharType'), 'separate')

    fldChar_end = OxmlElement('w:fldChar')
    fldChar_end.set(qn('w:fldCharType'), 'end')

    run_begin = OxmlElement('w:r')
    run_begin.append(fldChar_begin)
    toc_field.append(run_begin)

    run_instr = OxmlElement('w:r')
    run_instr.append(instrText)
    toc_field.append(run_instr)

    run_sep = OxmlElement('w:r')
    run_sep.append(fldChar_separate)
    toc_field.append(run_sep)

    # Placeholder text
    run_placeholder = OxmlElement('w:r')
    placeholder_text = OxmlElement('w:t')
    placeholder_text.text = '[Table of Contents will appear here - press F9 to update]'
    run_placeholder.append(placeholder_text)
    toc_field.append(run_placeholder)

    run_end = OxmlElement('w:r')
    run_end.append(fldChar_end)
    toc_field.append(run_end)

    parent.insert(insert_position, toc_field)
    insert_position += 1

    # Add page break after TOC
    page_break = OxmlElement('w:p')
    run = OxmlElement('w:r')
    br = OxmlElement('w:br')
    br.set(qn('w:type'), 'page')
    run.append(br)
    page_break.append(run)
    parent.insert(insert_position, page_break)


def remove_index_section(doc, index_idx):
    """
    Remove the Index section from the document.

    Removes Index heading and all subsequent paragraphs (Index content).

    Args:
        doc: Document object
        index_idx: Index of Index heading paragraph

    Returns:
        Number of paragraphs removed
    """
    if index_idx is None:
        return 0

    body = doc._element.body
    removed_count = 0

    # Find the Index heading element
    index_heading = doc.paragraphs[index_idx]._element
    heading_position = body.index(index_heading)

    # Remove everything from Index heading to end of document
    # (Index is always at the end)
    elements_to_remove = list(body[heading_position:])
    for elem in elements_to_remove:
        body.remove(elem)
        removed_count += 1

    return removed_count


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


def main():
    """Main function to prepare manuscript for KDP."""
    parser = argparse.ArgumentParser(
        description='Prepare manuscript for Kindle Direct Publishing (KDP)'
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
    print(f"Preparing for Kindle Direct Publishing (KDP)...\n")

    # Load document
    doc = Document(manuscript_path)

    # Step 1: Check for existing TOC
    toc_idx, toc_para = find_toc_heading(doc)

    if toc_idx is not None:
        print("✓ Found existing Table of Contents")

        # Add "toc" bookmark to TOC heading
        print("  → Adding 'toc' bookmark to TOC heading...")
        add_bookmark(toc_para, 'toc')

        # Remove page numbers from TOC field
        print("  → Removing page numbers from TOC (ebooks don't have page numbers)...")
        if remove_toc_page_numbers(doc, toc_idx):
            print("  ✓ TOC field updated for KDP format")
        else:
            print("  ⚠ TOC field not found - may need manual update")
    else:
        print("⚠ No Table of Contents found")
        print("  Creating KDP-compatible TOC...")

        try:
            copyright_idx = find_copyright_page_index(doc)
            create_kdp_toc(doc, copyright_idx, [])
            print("  ✓ KDP TOC created")
        except ValueError as e:
            print(f"  ✗ Error: {e}")
            print("  Skipping TOC creation")

    # Step 2: Remove Index section (not useful in ebooks)
    print("\n✓ Checking for Index section...")
    index_idx = find_index_heading(doc)

    if index_idx is not None:
        print("  → Found Index section")
        print("  → Removing Index (not useful in ebooks)...")
        removed = remove_index_section(doc, index_idx)
        print(f"  ✓ Removed Index section ({removed} elements)")
    else:
        print("  No Index section found (already removed or never added)")

    # Step 3: Save KDP-ready document
    timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M')
    filename = f"{book_short_name}-kdp-{timestamp}.docx"
    output_path = output_dir / filename

    doc.save(output_path)
    print(f"\n✓ Saved KDP-ready manuscript to: {output_path}")

    # Print next steps
    print("\n" + "="*60)
    print("KDP Preparation Complete!")
    print("="*60)
    print("\nNext steps:")
    print("  1. Open the document in Microsoft Word")
    print("  2. Press Ctrl+A (Select All)")
    print("  3. Press F9 (Update Fields) to populate TOC")
    print("  4. Verify:")
    print("     - TOC shows categories and books (NO page numbers)")
    print("     - TOC entries are clickable hyperlinks")
    print("     - No Index section at end")
    print("  5. Save as .docx")
    print("  6. Upload to Amazon KDP")
    print("\nKDP will convert .docx to Kindle format automatically.")
    print("="*60)


if __name__ == '__main__':
    main()
