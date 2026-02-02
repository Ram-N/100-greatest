# KDP (Kindle Direct Publishing) Preparation Guide


 Recommended Workflow

  The auto-detection is designed to follow this natural workflow:

  1. assemble_manuscript.py
     ↓ Creates: manuscript-2026-02-02-15-00.docx

  2. add_toc_and_index.py (auto-detects latest raw manuscript)
     ↓ Creates: manuscript-with-toc-2026-02-02-15-01.docx

  3. prepare_for_kdp.py (auto-detects latest with-toc)
     ↓ Creates: kdp-2026-02-02-15-02.docx

  Each step automatically picks up the output from the previous step!

## Overview

The `prepare_for_kdp.py` script converts a manuscript from PDF/print format to Kindle ebook format by:

1. ✅ Removing page numbers from TOC (ebooks don't have page numbers)
2. ✅ Adding "toc" bookmark to TOC heading (required by KDP)
3. ✅ Removing Index section (not useful in ebooks)
4. ✅ Optimizing for Kindle navigation with hyperlinks

## Quick Start

```bash
cd /home/ram/projects/100-greatest-series/books/travel-books
source ../../venv/bin/activate

# Auto-detect latest manuscript and prepare for KDP
python3 ../../shared/scripts/prepare_for_kdp.py

# Or specify a manuscript
python3 ../../shared/scripts/prepare_for_kdp.py \
  --manuscript output/travel-books-manuscript-with-toc-2026-02-01-22-34.docx
```

## Complete Publishing Workflow

### Step 1: Assemble Manuscript

```bash
python3 ../../shared/scripts/assembly/assemble_manuscript.py
```

**Output**: `travel-books-manuscript-2026-02-01-22-34.docx`

### Step 2A: For PDF/Print (with page numbers)

```bash
python3 ../../shared/scripts/add_toc_and_index.py
```

**Output**: `travel-books-manuscript-with-toc-2026-02-01-22-34.docx`

This version includes:
- TOC with page numbers
- Comprehensive Index with 1300+ entries
- Suitable for PDF export and print

### Step 2B: For Kindle/Ebook (no page numbers)

```bash
python3 ../../shared/scripts/prepare_for_kdp.py
```

**Output**: `travel-books-kdp-2026-02-01-22-34.docx`

This version includes:
- TOC without page numbers (hyperlinks only)
- "toc" bookmark (KDP requirement)
- No Index section (not useful in ebooks)
- Optimized for Kindle navigation

### Step 3: Update Fields in Word

**IMPORTANT**: This manual step is required for both versions.

1. Open the `.docx` file in Microsoft Word
2. Press **Ctrl+A** (Select All)
3. Press **F9** (Update Fields)
4. Save the document

### Step 4: Final Checks

**For PDF/Print version**:
- ✓ TOC shows categories, books, and page numbers
- ✓ Index appears at end with alphabetized entries
- ✓ All hyperlinks work

**For KDP/Ebook version**:
- ✓ TOC shows categories and books (NO page numbers)
- ✓ TOC entries are clickable hyperlinks
- ✓ No Index section at end
- ✓ "Contents" link in Kindle navigation menu

### Step 5: Export/Upload

**PDF/Print**:
1. File → Export → Create PDF/XPS
2. Save as `travel-books-final.pdf`

**Kindle/Ebook**:
1. Save the `.docx` file
2. Go to Amazon KDP (kdp.amazon.com)
3. Upload the `.docx` file directly
4. KDP will automatically convert to Kindle format

## What the Script Does

### Input

Accepts any manuscript file:
- Original assembled manuscript (without TOC/Index)
- Manuscript with TOC and Index (from `add_toc_and_index.py`)

### Processing

**1. TOC Modification**

If TOC exists:
- Adds "toc" bookmark to TOC heading
- Modifies TOC field code from:
  ```
  TOC \o "1-3" \h \z \u
  ```
  To:
  ```
  TOC \o "1-3" \h \n
  ```

Field switches explained:
- `\o "1-3"` - Include outline levels 1-3 (categories, books, authors)
- `\h` - Create hyperlinks
- `\n` - **No page numbers** (KDP requirement)
- ~~`\z`~~ - Removed (hide page numbers in web layout)
- ~~`\u`~~ - Removed (use paragraph outline level)

If TOC doesn't exist:
- Creates new KDP-compatible TOC after copyright page
- Includes "toc" bookmark
- Uses `\n` switch from the start

**2. Index Removal**

- Finds Index heading (Heading 1 style)
- Removes Index heading and all subsequent content
- Reduces file size
- Improves ebook reading experience

### Output

New file: `{book_short_name}-kdp-{timestamp}.docx`

Example: `travel-books-kdp-2026-02-02-12-45.docx`

## Command-Line Options

```bash
# Basic usage (auto-detect latest manuscript)
python3 ../../shared/scripts/prepare_for_kdp.py

# Specify manuscript file
python3 ../../shared/scripts/prepare_for_kdp.py \
  --manuscript output/travel-books-manuscript-with-toc-2026-02-01-22-34.docx

# Specify book root
python3 ../../shared/scripts/prepare_for_kdp.py \
  --book-root /path/to/book

# Show help
python3 ../../shared/scripts/prepare_for_kdp.py --help
```

## KDP Requirements

### 1. Table of Contents

Amazon KDP requires:
- ✅ TOC heading with "toc" bookmark (so Kindle can find it)
- ✅ No page numbers (ebooks don't have fixed page numbers)
- ✅ Hyperlinked entries (readers can click to navigate)
- ✅ Proper heading styles (Heading 1, 2, 3)

Our script handles all of this automatically.

### 2. Document Structure

**Heading Levels**:
- **Heading 1**: Category names (e.g., "Exploration at the Edge")
- **Heading 2**: Book titles (e.g., "The Great Railway Bazaar")
- **Heading 3**: Author names (e.g., "Paul Theroux")

This structure creates a hierarchical TOC that works well in Kindle's navigation menu.

### 3. File Format

Amazon KDP accepts:
- ✅ `.docx` (recommended - what our script produces)
- `.doc` (older format, not recommended)
- `.epub` (requires separate conversion)
- `.mobi` (deprecated)

**Our workflow**: Upload `.docx` directly to KDP, which converts it automatically.

## Why Two Separate Scripts?

### `add_toc_and_index.py` - PDF/Print Version

**Purpose**: Create professional reference guide with full navigation aids

**Features**:
- TOC with page numbers
- Comprehensive Index (1300+ entries: authors, locations, titles, keywords)
- Suitable for:
  - PDF export for digital distribution
  - Print-on-demand services
  - Desktop/tablet reading
  - Quick reference lookup

**Use when**: Publishing as PDF or print book

### `prepare_for_kdp.py` - Ebook Version

**Purpose**: Optimize for Kindle and ebook readers

**Features**:
- TOC without page numbers (ebooks have dynamic pagination)
- No Index (not useful in ebooks - readers use search instead)
- "toc" bookmark (Kindle navigation requirement)
- Smaller file size
- Suitable for:
  - Amazon Kindle
  - Kindle apps (iOS, Android, desktop)
  - Other ebook readers (via conversion)

**Use when**: Publishing to Amazon KDP or other ebook platforms

## Troubleshooting

### TOC Doesn't Update

**Problem**: TOC shows placeholder text or old content

**Solution**: Press F9 to update fields in Word

### "toc" Bookmark Not Found by Kindle

**Problem**: Kindle doesn't show "Contents" in navigation menu

**Causes**:
1. Bookmark wasn't added to TOC heading
2. Bookmark name is not exactly "toc" (case-sensitive)
3. Fields not updated before upload

**Solution**:
1. Run `prepare_for_kdp.py` script again
2. Verify script output shows "Adding 'toc' bookmark"
3. Press F9 in Word before uploading

### Index Still Appears in Ebook

**Problem**: Index section shows in Kindle preview

**Cause**: Script didn't find Index heading (wrong style or name)

**Solution**:
1. Check Index heading is styled as "Heading 1"
2. Check Index heading text is exactly "Index"
3. Run script again
4. Verify output shows "Removed Index section"

### TOC Shows Page Numbers in Kindle

**Problem**: Page numbers appear in TOC on Kindle device

**Cause**: TOC field still has `\z` or `\u` switches instead of `\n`

**Solution**:
1. Run `prepare_for_kdp.py` again
2. Check script output shows "TOC field updated for KDP format"
3. Open document in Word and verify TOC field code shows `\n` switch:
   - Right-click TOC
   - Toggle Field Codes (Alt+F9)
   - Should see: `{ TOC \o "1-3" \h \n }`

## Script Output Example

```
Processing: output/travel-books-manuscript-with-toc-2026-02-02-12-43.docx
Preparing for Kindle Direct Publishing (KDP)...

✓ Found existing Table of Contents
  → Adding 'toc' bookmark to TOC heading...
  → Removing page numbers from TOC (ebooks don't have page numbers)...
  ✓ TOC field updated for KDP format

✓ Checking for Index section...
  → Found Index section
  → Removing Index (not useful in ebooks)...
  ✓ Removed Index section (3 elements)

✓ Saved KDP-ready manuscript to: output/travel-books-kdp-2026-02-02-12-45.docx

============================================================
KDP Preparation Complete!
============================================================

Next steps:
  1. Open the document in Microsoft Word
  2. Press Ctrl+A (Select All)
  3. Press F9 (Update Fields) to populate TOC
  4. Verify:
     - TOC shows categories and books (NO page numbers)
     - TOC entries are clickable hyperlinks
     - No Index section at end
  5. Save as .docx
  6. Upload to Amazon KDP

KDP will convert .docx to Kindle format automatically.
============================================================
```

## Verification Checklist

Before uploading to KDP, verify:

- [ ] TOC heading says "Table of Contents"
- [ ] TOC has "toc" bookmark (check script output)
- [ ] TOC lists all categories and books
- [ ] TOC entries are hyperlinks (click to test)
- [ ] TOC has NO page numbers
- [ ] No Index section at end of document
- [ ] All heading styles are applied correctly (H1, H2, H3)
- [ ] Document saved as `.docx`
- [ ] Fields updated with F9

## KDP Upload Process

1. **Login**: Go to kdp.amazon.com
2. **Create New Title**: Click "Create New Title"
3. **Enter Metadata**: Title, author, description, keywords, categories
4. **Upload Manuscript**:
   - Click "Upload eBook manuscript"
   - Select your `{book}-kdp-{timestamp}.docx` file
   - KDP converts to Kindle format automatically
5. **Preview**: Use KDP's online previewer to check TOC navigation
6. **Pricing**: Set your price and royalty options
7. **Publish**: Click "Publish Your Kindle eBook"

## Advanced: Manual TOC Creation

If you prefer to create the TOC manually in Word (following KDP's instructions):

### Step 1: Apply Heading Styles

1. Highlight each category name
2. Home tab → Styles → Heading 1
3. Highlight each book title
4. Home tab → Styles → Heading 2

### Step 2: Insert TOC

1. Click after copyright page
2. References tab → Table of Contents → Automatic Table 1
3. References tab → Table of Contents → Custom Table of Contents
4. **Clear "Show Page Numbers" box**
5. Set "Show levels" to 2 (or 3 if you want author names)
6. Click OK

### Step 3: Add "toc" Bookmark

1. Highlight "Table of Contents" or "Contents" heading
2. Insert tab → Bookmark
3. Enter "toc" (lowercase, no quotes)
4. Click Add

### Step 4: Add Page Break

Insert → Page Break after TOC

**OR** just use our script and skip all this manual work! 🎉

## Dependencies

**Python packages** (already in venv):
- `python-docx` - Word document manipulation
- `pyyaml` - Config file loading

**No new dependencies required**.

## Summary

The `prepare_for_kdp.py` script provides:

✅ Automated KDP format conversion
✅ Removes page numbers from TOC (ebook requirement)
✅ Adds "toc" bookmark (Kindle navigation)
✅ Removes Index section (not useful in ebooks)
✅ Maintains hyperlink navigation
✅ Works with any manuscript (with or without existing TOC/Index)
✅ Professional ebook output suitable for Amazon KDP

**Key Difference from PDF Version**:
- PDF: TOC + Index with page numbers (reference guide)
- Ebook: TOC only without page numbers (optimized for Kindle)

---

**Script Location**: `/home/ram/projects/100-greatest-series/shared/scripts/prepare_for_kdp.py`

**Documentation**: `/home/ram/projects/100-greatest-series/shared/docs/KDP-PREPARATION.md`

**Last Updated**: 2026-02-02
