# Table of Contents and Index Generation

## Overview

The `add_toc_and_index.py` script is a post-processing tool that adds professional Table of Contents (TOC) and comprehensive Index sections to assembled manuscripts.

**Key Features**:
- ✅ Professional TOC with accurate page numbers and hyperlinks
- ✅ Comprehensive index covering authors, locations, titles, and keywords
- ✅ Uses Word field codes for accuracy (requires one manual F9 keypress)
- ✅ Prevents duplicate TOC/Index insertion
- ✅ Suitable for commercial ebook publication on Amazon KDP

## Quick Start

```bash
cd /home/ram/projects/100-greatest-series/books/travel-books
source ../../venv/bin/activate

# Add both TOC and Index (most common usage)
python3 ../../shared/scripts/add_toc_and_index.py

# The script will:
# 1. Auto-detect the latest manuscript
# 2. Insert TOC after copyright page
# 3. Extract and mark index entries
# 4. Insert Index at document end
# 5. Save new file with "-with-toc-" suffix
```

## How It Works

### Hybrid Field Code Approach

The script uses **Word field codes** instead of calculating page numbers in Python because:
- Page numbers can only be calculated by Word during rendering
- Field codes provide professional formatting
- Hyperlinks work automatically
- Output is suitable for commercial publishing

**Tradeoff**: Requires one manual step (pressing F9 in Word to update fields).

### TOC Generation

**Insertion Point**: After copyright page, before preface

**Field Code Used**: `TOC \o "1-3" \h \z \u`
- `\o "1-3"` - Include outline levels 1-3 (H1=categories, H2=books, H3=authors)
- `\h` - Create hyperlinks
- `\z` - Hide page numbers in web layout
- `\u` - Use paragraph outline level

**Output**: Hierarchical table with all 9 categories + 100+ books + authors

### Index Generation

The script automatically extracts four types of index entries from the assembled document:

1. **Authors** (from Heading 3) - e.g., "Polo, Marco"
2. **Locations** (from "Destinations Explored" bullets) - e.g., "Silk Road", "Beijing"
3. **Book Titles** (from Heading 2) - e.g., "The Travels"
4. **Keywords** (from "The Essentials" bullets) - e.g., "Buddhism", "Pilgrimage"

**Insertion Method**:
- Inserts hidden XE (Index Entry) fields throughout the document
- Inserts INDEX field code at document end: `INDEX \e " " \h "A" \c "2"`
  - `\e " "` - Separator between entry and page number
  - `\h "A"` - Heading style for letters
  - `\c "2"` - Two-column layout

**Output**: Professional alphabetized index with 1000+ entries

## Command-Line Options

### Basic Usage

```bash
# Auto-detect latest manuscript, add both TOC and Index
python3 ../../shared/scripts/add_toc_and_index.py

# Specify manuscript file
python3 ../../shared/scripts/add_toc_and_index.py \
  --manuscript output/travel-books-manuscript-2026-02-01-22-34.docx

# Specify book root (if not running from book directory)
python3 ../../shared/scripts/add_toc_and_index.py \
  --book-root /path/to/book
```

### Selective Addition

```bash
# Only add TOC (no index)
python3 ../../shared/scripts/add_toc_and_index.py --toc-only

# Only add Index (no TOC)
python3 ../../shared/scripts/add_toc_and_index.py --index-only
```

### All Options

```bash
python3 ../../shared/scripts/add_toc_and_index.py --help
```

```
usage: add_toc_and_index.py [-h] [--book-root BOOK_ROOT]
                            [--manuscript MANUSCRIPT] [--toc-only]
                            [--index-only]

Add Table of Contents and Index to assembled manuscript

options:
  -h, --help            show this help message and exit
  --book-root BOOK_ROOT
                        Path to book root directory (auto-detected if not
                        provided)
  --manuscript MANUSCRIPT
                        Path to manuscript file (auto-detects latest if not
                        provided)
  --toc-only            Only add Table of Contents
  --index-only          Only add Index
```

## Complete Workflow

### Step 1: Assemble Manuscript

```bash
cd /home/ram/projects/100-greatest-series/books/travel-books
source ../../venv/bin/activate
python3 ../../shared/scripts/assembly/assemble_manuscript.py
```

Output: `output/travel-books-manuscript-2026-02-01-22-34.docx`

### Step 2: Add TOC and Index

```bash
python3 ../../shared/scripts/add_toc_and_index.py
```

Output: `output/travel-books-manuscript-with-toc-2026-02-01-23-15.docx`

Console output:
```
Processing: output/travel-books-manuscript-2026-02-01-22-34.docx

Inserting Table of Contents field...
✓ TOC field inserted after copyright page

Extracting index entries...
Found 111 authors, 411 locations, 732 keywords, 110 titles
Inserting XE index fields...
✓ 1364 index entries marked

Inserting INDEX field at end...
✓ Index field inserted

✓ Saved to: output/travel-books-manuscript-with-toc-2026-02-01-23-15.docx

============================================================
Next steps:
  1. Open the document in Microsoft Word
  2. Press Ctrl+A (Select All)
  3. Press F9 (Update Fields)
  4. Save and export to PDF for publishing
============================================================
```

### Step 3: Update Fields in Word

**IMPORTANT**: This manual step is required for page numbers to appear.

1. Open `travel-books-manuscript-with-toc-2026-02-01-23-15.docx` in Microsoft Word
2. Press **Ctrl+A** (Select All) to select entire document
3. Press **F9** (Update Fields) to populate TOC and Index with page numbers
4. Save the document

**Result**: TOC and Index now show accurate page numbers and hyperlinks work.

### Step 4: Export to PDF

1. File → Export → Create PDF/XPS
2. Save as `travel-books-final.pdf`
3. Upload to Amazon KDP

## Duplicate Prevention

The script automatically detects if TOC or Index already exists:

```bash
python3 ../../shared/scripts/add_toc_and_index.py \
  --manuscript output/travel-books-manuscript-with-toc-2026-02-01-23-15.docx
```

Output:
```
⚠ Table of Contents already exists in document. Skipping TOC insertion.
  To regenerate, use the original manuscript without TOC.

⚠ Index already exists in document. Skipping Index insertion.
  To regenerate, use the original manuscript without Index.
```

**To regenerate**: Always use the original manuscript (without `-with-toc-` in filename).

## Validation

To verify the generated document:

```bash
source ../../venv/bin/activate
python3 << 'EOF'
from docx import Document

doc = Document('output/travel-books-manuscript-with-toc-2026-02-02-09-46.docx')

toc_found = any(
    'Table of Contents' in p.text and p.style and 'Heading' in p.style.name
    for p in doc.paragraphs
)

index_found = any(
    p.text.strip() == 'Index' and p.style and 'Heading' in p.style.name
    for p in doc.paragraphs
)

print(f"TOC present: {'✓' if toc_found else '✗'}")
print(f"Index present: {'✓' if index_found else '✗'}")
EOF
```

## Customization

### Changing TOC Depth

Edit the `TOC` field code pattern in `insert_toc_field()`:

```python
instrText.text = ' TOC \\o "1-3" \\h \\z \\u '
#                              ^^^
#                         Change to "1-2" for shallower TOC
#                         Change to "1-4" for deeper TOC
```

### Changing Index Layout

Edit the `INDEX` field code pattern in `insert_index_field()`:

```python
instrText.text = ' INDEX \\e " " \\h "A" \\c "2" '
#                                            ^^^
#                                       Change to "3" for 3 columns
#                                       Remove \\c "2" for single column
```

### Adding More Index Entry Types

1. Add extraction logic to `extract_index_entries()`
2. Add new category to `index_entries` dictionary
3. Entries will automatically be marked with XE fields

Example: Adding a "Publishers" index:

```python
# In extract_index_entries():
index_entries = {
    'authors': [],
    'locations': [],
    'titles': [],
    'keywords': [],
    'publishers': []  # New category
}

# Add extraction logic:
elif in_essentials and 'Publisher' in text:
    publisher = extract_publisher(text)
    index_entries['publishers'].append((publisher, i))
```

## Technical Details

### XML Field Structure

**TOC Field**:
```xml
<w:p>
  <w:r>
    <w:fldChar w:fldCharType="begin"/>
  </w:r>
  <w:r>
    <w:instrText xml:space="preserve"> TOC \o "1-3" \h \z \u </w:instrText>
  </w:r>
  <w:r>
    <w:fldChar w:fldCharType="end"/>
  </w:r>
</w:p>
```

**Index Entry Field** (hidden):
```xml
<w:p>
  <w:r>
    <w:rPr>
      <w:vanish/>  <!-- Hidden text -->
    </w:rPr>
    <w:fldChar w:fldCharType="begin"/>
  </w:r>
  <w:r>
    <w:instrText> XE "Parkman, Francis" </w:instrText>
  </w:r>
  <w:r>
    <w:fldChar w:fldCharType="end"/>
  </w:r>
</w:p>
```

**INDEX Field**:
```xml
<w:p>
  <w:r>
    <w:fldChar w:fldCharType="begin"/>
  </w:r>
  <w:r>
    <w:instrText xml:space="preserve"> INDEX \e " " \h "A" \c "2" </w:instrText>
  </w:r>
  <w:r>
    <w:fldChar w:fldCharType="end"/>
  </w:r>
</w:p>
```

### Dependencies

**Required Python packages** (already in venv):
- `python-docx` - Word document manipulation
- `pyyaml` - Config file loading (via book_utils)

**No new dependencies required**.

### Error Handling

**No manuscript found**:
```
FileNotFoundError: No manuscript found matching: travel-books-manuscript-*.docx
Run assemble_manuscript.py first.
```

**Invalid document structure**:
```
ValueError: Invalid manuscript: No book entries (Heading 2) found.
```

**Copyright page not found**:
```
Warning: Copyright page not found in manuscript.
Skipping TOC insertion
```

In this case, Index is still added, but TOC insertion is skipped.

## Output Files

**Naming Convention**: `{book_short_name}-manuscript-with-toc-{timestamp}.docx`

**Example**: `travel-books-manuscript-with-toc-2026-02-02-09-46.docx`

**Location**: Same `output/` directory as original manuscript

**Size**: Approximately 10-20KB larger than original (due to hidden XE fields)

## Troubleshooting

### Page Numbers Don't Show

**Problem**: TOC or Index shows field codes instead of page numbers.

**Solution**: Press F9 to update fields in Word.

### TOC Doesn't Include All Books

**Problem**: Some books missing from TOC.

**Cause**: Books don't have proper Heading 2 style applied.

**Solution**: Check manuscript assembly - all book titles should use Heading 2.

### Index Is Empty

**Problem**: Index field exists but shows no entries.

**Cause**: XE fields not inserted or F9 not pressed.

**Solution**:
1. Verify script output shows "X index entries marked"
2. Press F9 to update fields in Word

### Duplicate TOC/Index Sections

**Problem**: Multiple TOC or Index sections in document.

**Cause**: Script run multiple times on same document.

**Solution**: Use original manuscript (without `-with-toc-` suffix) as input.

### Location/Keyword Extraction Misses Entries

**Problem**: Expected locations or keywords don't appear in index.

**Cause**: Format doesn't match extraction patterns.

**Debug**:
```bash
# Check actual bullet format
source ../../venv/bin/activate
python3 << 'EOF'
from docx import Document
doc = Document('output/manuscript.docx')
for i, para in enumerate(doc.paragraphs):
    if 'Destinations' in para.text and para.style.name == 'Heading 4':
        # Print next 5 bullets
        for j in range(i+1, min(i+6, len(doc.paragraphs))):
            if doc.paragraphs[j].style.name == 'List Bullet':
                print(f"{j}: {doc.paragraphs[j].text[:80]}")
        break
EOF
```

**Solution**: Adjust extraction patterns in `extract_location()` or `extract_keywords()`.

## Future Enhancements

**Phase 2 (optional improvements)**:

1. **Multiple indexes** - Separate author/location/subject indexes
2. **Subentries** - "Alaska → Stampede Trail, 45"
3. **Cross-references** - "See also" entries
4. **Page ranges** - "Alaska, 23-45" instead of "Alaska, 23, 24, 25..."
5. **Custom TOC styles** - More formatting control
6. **Auto-update** - Trigger F9 programmatically (platform-specific)

## Summary

The `add_toc_and_index.py` script provides:

✅ Professional TOC with accurate page numbers and hyperlinks
✅ Comprehensive index covering 4 data types (1000+ entries)
✅ Minimal manual steps (single F9 keypress in Word)
✅ Suitable for commercial ebook publication on Amazon KDP
✅ Reusable across all books in the 100 Greatest Series
✅ Maintains full document editability

**Key Tradeoff**: Requires one manual step (F9 to update fields) but provides professional, accurate output suitable for commercial publishing.

---

**Script Location**: `/home/ram/projects/100-greatest-series/shared/scripts/add_toc_and_index.py`

**Documentation**: `/home/ram/projects/100-greatest-series/shared/docs/TOC-AND-INDEX.md`

**Last Updated**: 2026-02-02
