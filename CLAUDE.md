# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

The **100 Greatest Series** is a multi-book publishing project creating curated reference guides to essential works across different genres. Each book presents 100 carefully selected titles with rich two-page spreads, designed for ebook distribution via Amazon KDP.

**Current Project**: The 100 Greatest Travel Books Ever Written (123 entries complete, 9 thematic categories)

**Future Projects**: History books, biographies, and other genres

## Repository Structure

```
100-greatest-series/
├── shared/                          # Shared infrastructure (all books use these)
│   ├── scripts/                     # Python automation scripts
│   │   ├── book_utils.py           # Config loading and path detection
│   │   ├── assemble_manuscript.py  # Word doc assembly
│   │   ├── recommend_next.py       # Book recommendation engine
│   │   ├── check_book.py           # Database search
│   │   ├── update_status.py        # Sync database with completed writeups
│   │   ├── change_status.py        # Batch status updates
│   │   ├── organize_books.py       # File organization
│   │   └── validate_manuscript.py  # Structure validation
│   ├── templates/                   # Entry templates
│   ├── schemas/                     # Database schemas
│   └── docs/                        # Series-wide documentation
│
└── books/                           # Individual book projects
    └── travel-books/                # The 100 Greatest Travel Books
        ├── config.yaml              # Book configuration (categories, paths, metadata)
        ├── book-writeups/           # 123 completed entries in 9 categories
        ├── database/                # CSV databases with candidates and metadata
        ├── templates/               # Book-specific templates
        ├── introduction/            # Front matter
        ├── assembly/                # Assembly instructions
        └── output/                  # Generated manuscripts
```

## Key Commands

All commands assume you're in a book directory (e.g., `books/travel-books/`). Scripts auto-detect the book root by finding `config.yaml`.

### Core Workflow Commands

```bash
# Navigate to travel books project
cd /home/ram/projects/100-greatest-series/books/travel-books

# Assemble complete manuscript into Word document
python3 ../../shared/scripts/assemble_manuscript.py

# Get intelligent recommendations for which books to write next
python3 ../../shared/scripts/recommend_next.py --limit 10

# Search the candidate database
python3 ../../shared/scripts/check_book.py "Into the Wild"

# Sync database status with completed writeup files
python3 ../../shared/scripts/update_status.py --apply

# Batch update book statuses
python3 ../../shared/scripts/change_status.py "Wild" "Completed"

# Project status dashboard (bash script specific to travel-books)
./status.sh                    # Full dashboard
./status.sh --view completed   # List completed entries
```

### Python Dependencies

Required packages:
- `pyyaml` - Configuration file loading
- `python-docx` - Word document generation
- `pandas` - Optional, for advanced database operations

Installation:
```bash
# Use existing venv from original project
source /home/ram/projects/100TravelBooks/venv/bin/activate

# Or create new venv
cd /home/ram/projects/100-greatest-series
python3 -m venv venv
source venv/bin/activate
pip install pyyaml python-docx pandas
```

## Architecture & Design

### Config-Driven Structure

Each book has a `config.yaml` defining:
- **Book metadata**: Title, short name, target count
- **Directory structure**: Where databases, writeups, and output live
- **Category system**: Thematic organization with IDs and names
- **Database files**: Candidates, selections, progress tracking
- **Assembly order**: How to compile the manuscript

This config-driven approach allows scripts to work with any book in the series without modification.

### Auto-Detection System

Scripts use `book_utils.py` to automatically:
1. Walk up directory tree to find `config.yaml` (the book root marker)
2. Load book configuration
3. Resolve all relative paths
4. Support manual override with `--book-root` parameter

### Database Schema

Travel books use CSV databases with comprehensive metadata:
- **Identity tracking**: Author gender, indigenous voices, BIPOC representation
- **Geographic indexing**: Multi-continent coverage (pipe-separated tags)
- **Selection workflow**: Status field (Candidate/Selected/Completed/Cut/HonorableMention)
- **Quality tiers**: 4-tier system (bestsellers → travel canon → deep divers → wildcards)
- **Diversity metrics**: Tracks representation across multiple dimensions

### Entry Template System

Standardized two-page format ensures consistency:
1. **Title & Quote** - Memorable opening
2. **The Essentials** - Genre, keywords, traveler profile archetype
3. **The Author** - Biographical sketch (100-150 words)
4. **The Book** - Journey and significance (150-200 words)
5. **Destinations Explored** - Geographic coverage with evocative descriptions
6. **Further Reading** - Related recommendations
7. **The Signature Line** - Defining quote
8. **The Perfect Pairing** - Atmospheric details (drink, soundtrack, setting)

Target length: 300-500 words (excluding quotes and lists)

### Category System

Travel books organize entries into 9 thematic categories:
1. First Routes and Foundational Journeys
2. Exploration at the Edge
3. Slow Routes and Long Ways Through
4. Frontiers and Frictions
5. Humbled by the World
6. Institutional Constraints
7. Inhabited Landscapes
8. Political Moral and Historical Reckonings
9. Self-Reckoning Through Movement

Categories are defined in `config.yaml` and drive directory structure, manuscript assembly, and recommendation engine.

### Manuscript Assembly

The `assemble_manuscript.py` script:
- Reads assembly order from `assembly/Order-of-assembly.md`
- Collects introduction, category intros, and book entries
- Generates formatted Word document with proper styling
- Outputs to configured `output_dir`
- Processes 100+ entries in seconds

### Recommendation Engine

The `recommend_next.py` script analyzes:
- **Diversity gaps**: Prioritizes underrepresented voices (BIPOC, indigenous, women)
- **Geographic coverage**: Identifies missing regions (Caribbean, South America, Africa, Oceania)
- **Tier distribution**: Balances quality across bestsellers to wildcards
- **Author variety**: Prevents overrepresentation of any single author
- **Category balance**: Ensures even distribution across themes

Outputs scored, ranked recommendations with explanations.

## Starting a New Book

Complete guide in `shared/docs/STARTING-NEW-BOOK.md`. Quick steps:

1. Copy structure from `books/travel-books/`
2. Clear out content (keep directories)
3. Create new `config.yaml` with your categories
4. Initialize database CSVs
5. Update CLAUDE.md for book-specific context
6. Start writing

All shared scripts automatically work with the new book once configured.

## Writing Style Guidelines

For travel books (adapt for other genres):
- **Encyclopedic but engaging**: Informative without being academic
- **Accessible**: Intelligent but not requiring specialized knowledge
- **Rich context**: Historical, cultural, and literary significance
- **Practical guidance**: Help readers decide if book suits them
- **NO emojis** unless explicitly requested
- **Concise**: Every word earns its place

## Important Constraints

### Copyright & Fair Use
- Keep quotes short (1-2 sentences maximum)
- Always attribute properly
- This is transformative commentary/criticism (defensible fair use)
- **NO book cover images** unless Creative Commons/open source
- Cannot screenshot from Amazon for commercial use

### Commercial Viability
- Target: Amazon KDP (PDF and EPUB formats)
- Two-page spreads must work in digital scrolling format
- Pricing and marketing considerations for self-publishing
- Professional quality essential for competitive marketplace

## Project Status

### Travel Books
- **Status**: Content complete (123 entries written)
- **Phase**: Assembly and refinement
- **Timeline**: Originally 1 month to production
- **Current**: Organizing categories, finalizing manuscript

### Future Books
- History books (planned)
- Biographies (planned)
- Other genres (TBD)

## Working Principles

1. **Simplicity first**: Warn if simpler options exist
2. **Batch operations**: Work on multiple entries in parallel when possible
3. **Preserve user's voice**: Don't over-edit existing writeups
4. **Research thoroughly**: Use WebSearch for facts, quotes, critical reception
5. **Balance dimensions**: Consider diversity across all criteria (geography, era, gender, race, genre)
6. **Config-driven design**: All book-specific details belong in `config.yaml`, not hardcoded in scripts

## Script Reference

### assemble_manuscript.py
Compiles complete manuscript from individual entries into Word document. Uses assembly order file and category structure from config.

### recommend_next.py
Intelligent recommendation engine suggesting which books to write next based on diversity gaps, geographic coverage, and quality distribution.

### check_book.py
Database search tool supporting substring, token, and regex modes. Exports results to CSV.

### update_status.py
Syncs database Status field with actual completed writeup files. Creates backups before making changes.

### change_status.py
Batch updates book statuses in database.

### organize_books.py
File organization utility for managing book entries across categories.

### validate_manuscript.py
Validates manuscript structure against expected format.

### book_utils.py
Core utilities for path detection and config loading. All other scripts depend on this.

## Migration History

This project was refactored from a standalone repository (`/home/ram/projects/100TravelBooks`) into a series structure on 2026-01-30. Full migration details in `MIGRATION-SUMMARY.md`.

Key changes:
- Centralized shared scripts
- Config-driven categories (no more hardcoding)
- Auto-detection of book root
- Series-level infrastructure for future books

Original project remains intact at `/home/ram/projects/100TravelBooks` for backup purposes.

---

**Last Updated**: 2026-01-30
