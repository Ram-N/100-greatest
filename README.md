# 100 Greatest Series

A multi-book series of curated guides to the finest works in various genres, designed as ebooks for Amazon KDP.

## Structure

This repository contains multiple "100 Greatest" books sharing common infrastructure:

```
100-greatest-series/
├── shared/               # Shared infrastructure for all books
│   ├── scripts/         # Python scripts and utilities
│   ├── templates/       # Entry templates
│   ├── schemas/         # Database schemas
│   └── docs/            # Series-wide documentation
│
└── books/               # Individual book projects
    ├── travel-books/    # The 100 Greatest Travel Books
    ├── history-books/   # (Future) The 100 Greatest History Books
    └── biographies/     # (Future) The 100 Greatest Biographies
```

## Current Books in Series

### 1. Travel Books (Active)
**Status**: Content complete (123 entries across 9 categories)
**Location**: `books/travel-books/`
**Target**: 100 main entries + honorable mentions

## Shared Scripts

All books in the series use the same set of scripts located in `shared/scripts/`:

- **assemble_manuscript.py** - Assemble book entries into Word document
- **recommend_next.py** - Intelligent recommendation engine for next books to write
- **check_book.py** - Search database for books
- **update_status.py** - Sync database with completed writeups
- **change_status.py** - Batch update book statuses
- **validate_manuscript.py** - Validate manuscript structure
- **organize_books.py** - Organize book files
- **book_utils.py** - Shared utilities for path detection and config loading

### Using Scripts

All scripts auto-detect the book root by looking for `config.yaml`. Run from within any book directory:

```bash
cd books/travel-books
python3 ../../shared/scripts/assemble_manuscript.py
python3 ../../shared/scripts/recommend_next.py --limit 10
python3 ../../shared/scripts/check_book.py "Into the Wild"
```

Or specify the book root manually:

```bash
python3 shared/scripts/check_book.py --book-root books/travel-books "Africa"
```

## Starting a New Book

See `shared/docs/STARTING-NEW-BOOK.md` for a complete guide.

Quick start:
1. Copy the template structure from an existing book
2. Create `config.yaml` with your book's settings
3. Define your category system
4. Initialize your database CSVs
5. Start writing entries

## Dependencies

### Python Requirements
- Python 3.8+
- PyYAML (for config loading)
- python-docx (for manuscript assembly)
- pandas (optional, for advanced database operations)

### Installation

Using the existing venv from original location:
```bash
source /home/ram/projects/100TravelBooks/venv/bin/activate
pip install pyyaml  # if not already installed
```

Or create a new venv for the series:
```bash
cd 100-greatest-series
python3 -m venv venv
source venv/bin/activate
pip install pyyaml python-docx pandas
```

## Git Strategy

Single repository for entire series:
- All books share git history
- Shared infrastructure changes benefit all books
- Easy to track cross-book improvements

## Book Configuration

Each book has a `config.yaml` file defining:
- Book title and metadata
- Directory structure
- Category system
- Database file names
- Assembly order

Example:
```yaml
book:
  title: "The 100 Greatest Travel Books Ever Written"
  short_name: "travel-books"
  target_count: 100

structure:
  database_dir: "database"
  writeups_dir: "book-writeups"
  assembly_dir: "assembly"

categories:
  - id: "1_first_routes"
    name: "First Routes and Foundational Journeys"
  - id: "2_exploration"
    name: "Exploration at the Edge"
```

## License

© 2026 - All rights reserved

## Author

Ram Rachum
