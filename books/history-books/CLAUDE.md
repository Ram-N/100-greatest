# CLAUDE.md

This file provides guidance to Claude Code when working on **The 100 Greatest History Books Ever Written** project.

## Project Overview

A curated guide to the finest history books, designed as an ebook (PDF/EPUB) for sale on Amazon KDP. Each of the 100 books gets a two-page spread with rich detail to help readers discover essential historical works.

**Target Audience**: History enthusiasts, students, general readers seeking authoritative and engaging historical narratives
**Format**: PDF and EPUB for Amazon KDP
**Current Status**: Initial setup, beginning candidate collection

## Core Concept

This is an encyclopedic yet engaging reference guide with:
- Historical scholarship and readability as primary selection criteria
- Mix of academic classics, popular narratives, microhistories, and biographical works
- Coverage from ancient history through contemporary
- Global geographic coverage (not Euro/US-centric)
- Diverse voices: women historians, BIPOC scholars, non-Western perspectives
- Multiple indexing systems (era, region, type of history, narrative style)

## Project Structure

**NOTE**: This project is part of the "100 Greatest Series" monorepo.

```
/home/ram/projects/100-greatest-series/
├── shared/                      # Shared infrastructure
│   ├── scripts/                # Python scripts (all books use these)
│   ├── templates/              # Entry templates
│   ├── schemas/                # Series-wide schemas
│   └── docs/                   # Series-wide documentation
│
└── books/history-books/        # THIS PROJECT
    ├── config.yaml             # Book configuration
    ├── CLAUDE.md               # This file
    ├── database/               # CSV databases and schema
    │   ├── database-schema.json        # Machine-readable schema
    │   ├── master-candidates.csv       # All candidates
    │   ├── README-DATABASE.md          # Database documentation
    │   └── (other CSV files as needed)
    ├── candidate-books/        # Initial candidate lists
    ├── book-writeups/          # Completed entries (organized by category)
    ├── templates/              # Book-specific templates
    ├── introduction/           # Front matter
    ├── assembly/               # Assembly instructions
    └── output/                 # Generated manuscripts
```

## Database Schema

The database uses a JSON schema (`database/database-schema.json`) with these key fields:

### Essential Fields:
- **ID** - Unique identifier
- **Status** - Candidate / Selected / HonorableMention / Cut / Completed
- **Title**, **Author**, **Year**
- **author_gender**, **author_person_of_color**, **author_indigenous**
- **time_period_covered** - Historical period (e.g., "1914-1918", "Ancient Rome")
- **era_category** - Ancient / Medieval / Early Modern / 19th C / 20th C / 21st C / Multiple
- **geographic_scope** - Pipe-separated regions (e.g., "Europe|Asia")
- **history_type** - Military / Political / Social / Cultural / Economic / etc.
- **narrative_style** - Academic / Popular / Microhistory / Biography / etc.
- **Tier** - 1-4 quality system (1=Pulitzer winners, 4=wildcards)

### History-Specific Fields:
- **historiographical_approach** - Scholarly school/method
- **primary_sources** - yes/no/mixed
- **awards** - Pulitzer, National Book Award, etc.
- **reader_archetype** - Who this book is for
- **accessibility** - Easy / Moderate / Challenging / Very Challenging

See `database/database-schema.json` for complete specifications.

## Selection Criteria

We're building from candidates to 100 using these balanced criteria:

### Must Include:
- **Scholarly merit**: Original research, influential arguments, well-sourced
- **Readability**: Engaging narrative, accessible (not just for specialists)
- **Historical significance**: Impact on the field, shaped how we understand a period
- **Geographic diversity**: Not Euro/US-centric; include Africa, Asia, Latin America, Middle East
- **Temporal diversity**: Ancient through contemporary, not dominated by WWII
- **Voice diversity**: Women historians, BIPOC scholars, non-Western perspectives
- **Type variety**: Not all military or political; include social, cultural, economic, biographical

### Nice to Have:
- Awards (Pulitzer, National Book Award)
- Still in print and accessible
- Modern relevance
- Primary source usage

### Four-Tier System:
1. **Defining Works** - Pulitzer winners, household names, genre-defining (25-30 books)
2. **Essential Reading** - Scholarly canon, widely cited, influential (35-40 books)
3. **Deep Dives** - Specialist favorites, important but narrower focus (20-25 books)
4. **Wildcards** - Newer works, niche topics, controversial perspectives (10-15 books)

## Categories

Initial thematic categories (flexible, may evolve):
1. Ancient Civilizations and Classical History
2. Medieval and Renaissance
3. Revolutions and Nation-Building
4. Wars and Military History
5. Social and Cultural History
6. Biographical and Personal Histories
7. Global and Comparative History
8. Modern and Contemporary History

## Writing Style & Tone

- **Encyclopedic but engaging**: Not dry academic prose, but authoritative
- **Accessible**: Work for both history buffs and general readers
- **Rich with context**: Scholarly significance, historical debates, why it matters
- **Practical guidance**: Help readers decide if this book is for them
- **NO emojis** unless explicitly requested
- **Concise**: Two-page limit per book (approximately 300-500 words)

## Entry Template Structure

Each book entry follows a consistent format (to be developed, based on travel books template):

### Likely Sections:
1. **Title & Author** - with memorable quote
2. **The Essentials** - Era, type, keywords, reader archetype
3. **The Historian** - Brief biographical sketch, scholarly approach
4. **The Book** - What period/topic covered, main argument, significance
5. **Historical Scope** - Geographic and temporal coverage
6. **Further Reading** - Related books (within and outside the 100)
7. **The Signature Line** - Defining quote from the book
8. **The Perfect Pairing** - Atmospheric details

Target length: 300-500 words (excluding quotes and lists)

## Diversity Targets

### Author Identity:
- Women historians: ≥30%
- BIPOC scholars: ≥20%
- Indigenous historians: Include where possible
- Non-Western perspectives: Meaningful representation

### Geographic Scope:
- Not Euro/US-centric
- Include Africa, Asia, Latin America, Middle East, Oceania
- Global and comparative works

### Temporal Coverage:
- Ancient (pre-500 CE)
- Medieval (500-1500)
- Early Modern (1500-1800)
- 19th Century
- 20th Century
- 21st Century
- Not dominated by any single era (especially WWII)

### Type of History:
- Military, Political, Social, Cultural, Economic
- Biographical, Environmental, Intellectual, Religious
- Women's History, Labor History, Colonial/Imperial

## Running Scripts

All scripts are in `../../shared/scripts/` and auto-detect the book root via `config.yaml`:

```bash
cd /home/ram/projects/100-greatest-series/books/history-books

# Check database for a book
python3 ../../shared/scripts/check_book.py "Guns of August"

# Get recommendations for which books to write next
python3 ../../shared/scripts/recommend_next.py --limit 10

# Update database status from completed writeups
python3 ../../shared/scripts/update_status.py --apply

# Assemble manuscript (when ready)
python3 ../../shared/scripts/assembly/assemble_manuscript.py
```

### Script Dependencies

Use the series venv:
```bash
source ../../venv/bin/activate
```

Or install dependencies:
```bash
pip install pyyaml python-docx pandas
```

## Working Principles

1. **Simplicity first**: Warn if simpler options exist
2. **Batch operations**: Work on multiple entries in parallel when possible
3. **Research thoroughly**: Use WebSearch for facts, quotes, awards, critical reception
4. **Balance dimensions**: Consider diversity across all criteria (geography, era, gender, race, type)
5. **Config-driven design**: All book-specific details belong in `config.yaml`

## Current Phase

**Phase**: Initial setup and candidate collection
**Immediate Tasks**:
1. Import candidates from comet1.md and other sources
2. Build master-candidates.csv with 150-200 candidates
3. Research basic metadata (Year, Tier, awards, author identity)
4. Begin selection process - mark obvious "Selected" choices
5. Check balance and fill gaps
6. Narrow to final 100

## Notes & Reminders

- User wants to sell on Amazon KDP - keep commercial viability in mind
- PDF and EPUB both needed
- Two-page spreads need to work in digital format
- Timeline TBD (can reference travel books: 1 month timeline)
- Expect difficult choices between similar books (e.g., multiple WWII books)

---

**Last Updated**: 2026-02-10
**Project Phase**: Initial Setup
