# History Books Project Setup Summary

**Date Created**: 2026-02-10

## What Was Created

### 1. Directory Structure

Fixed typo (`hisotry-books` → `history-books`) and created standard structure:

```
history-books/
├── CLAUDE.md                    # Project-specific guidance for Claude
├── SETUP-SUMMARY.md             # This file
├── config.yaml                  # Book configuration
├── assembly/                    # Assembly instructions (empty for now)
├── book-writeups/               # Completed entries (empty for now)
├── candidate-books/             # Initial candidate lists (has comet1.md)
├── database/                    # Database files
│   ├── database-schema.json    # Machine-readable schema
│   ├── master-candidates.csv   # Main database (headers only)
│   └── README-DATABASE.md      # Database documentation
├── introduction/                # Front matter (empty for now)
├── output/                      # Generated manuscripts (empty for now)
└── templates/                   # Book-specific templates (empty for now)
```

### 2. Database Schema (database-schema.json)

**Machine-readable JSON schema** with:
- 24 field definitions with types, validation rules, and examples
- Enumerated values for dropdown fields
- Diversity targets (30% women, 20% BIPOC)
- Workflow statuses (Candidate → Selected → Completed)
- Validation rules for data quality
- CSV export column order

**Key Adaptations from Travel Books:**
- Replaced `travel_continents` with `geographic_scope` (regions covered)
- Replaced `travel_mode` with `history_type` (Military, Social, Cultural, etc.)
- Added `time_period_covered` (e.g., "1914-1918")
- Added `era_category` (Ancient, Medieval, 19th C, 20th C, etc.)
- Added `narrative_style` (Academic, Popular, Microhistory, etc.)
- Added `historiographical_approach` (scholarly school/method)
- Added `primary_sources` (yes/no/mixed)
- Added `awards` (Pulitzer, National Book Award, etc.)
- Added `accessibility` (Easy to Very Challenging)
- Added `reader_archetype` (who the book is for)

### 3. CSV Database (master-candidates.csv)

**Headers match schema exactly:**
```
ID,Status,Title,Author,author_gender,author_indigenous,author_person_of_color,
author_identity_notes,Year,time_period_covered,era_category,geographic_scope,
Primary_Region,history_type,narrative_style,historiographical_approach,
primary_sources,Tier,awards,reader_archetype,page_count,accessibility,
Source,Notes
```

Ready to import candidates from comet1.md or other sources.

### 4. Documentation (README-DATABASE.md)

**Comprehensive guide covering:**
- Field definitions and usage
- Selection process (4-step workflow)
- Diversity balancing strategies
- History-specific considerations
- Quality tier guidelines
- How to populate author identity fields
- Next steps for getting started

### 5. Configuration (config.yaml)

**Book-specific config** with:
- Book metadata (title, target count)
- Directory structure mapping
- 8 initial thematic categories (flexible, can evolve)
- Database file paths
- Assembly configuration
- Reference to schema file

### 6. Project Documentation (CLAUDE.md)

**Project-specific guidance** covering:
- Project overview and goals
- Database schema summary
- Selection criteria and diversity targets
- Category system
- Writing style guidelines
- How to run shared scripts
- Current phase and immediate tasks

## Key Differences from Travel Books

### Conceptual:
- History books focus on **historical scholarship + readability**
- Travel books focus on **journey narrative + literary merit**

### Fields Unique to History:
- `time_period_covered` - What historical period is covered
- `era_category` - Broad categorization (Ancient, Medieval, etc.)
- `history_type` - Type of history (Military, Social, Cultural, etc.)
- `narrative_style` - Writing approach (Academic, Popular, Microhistory)
- `historiographical_approach` - Scholarly method/school
- `primary_sources` - Whether book uses primary sources
- `awards` - Pulitzers and other major awards
- `accessibility` - Reading difficulty level

### Fields Removed/Adapted:
- ~~`travel_continents`~~ → `geographic_scope` (still relevant for history)
- ~~`travel_mode`~~ → Not applicable
- ~~`journey_year`~~ → `time_period_covered` instead
- ~~`traveler_profile`~~ → `reader_archetype` (who should read this)

### Categories:
- Travel books: 9 thematic categories (First Routes, Exploration, etc.)
- History books: 8 initial categories (Ancient, Medieval, Wars, etc.)
- Categories for history are more flexible and may evolve

## Next Steps

### Immediate (Setup Phase):
1. ✅ Fix directory typo
2. ✅ Create database schema (JSON)
3. ✅ Create CSV database with headers
4. ✅ Write documentation
5. ✅ Create config.yaml
6. ✅ Create CLAUDE.md

### Phase 1: Candidate Collection
1. Import candidates from `candidate-books/comet1.md`
2. Gather candidates from:
   - Pulitzer Prize lists (History category)
   - National Book Award lists
   - AI recommendations
   - Personal reading lists
   - Award-winning historians
3. Populate master-candidates.csv with 150-200 candidates
4. Add basic metadata: Title, Author, Year, Tier

### Phase 2: Research & Metadata
1. Research author identity fields (gender, BIPOC, indigenous)
2. Add time periods, geographic scope, history types
3. Note awards and accessibility levels
4. Document sources in author_identity_notes

### Phase 3: Selection
1. Mark obvious "Selected" candidates (Pulitzer winners, classics)
2. Check diversity balance (geography, era, author identity, type)
3. Fill gaps based on analysis
4. Narrow to final 100

### Phase 4: Content Creation
1. Develop entry template (adapt from travel books)
2. Begin writing entries
3. Use recommend_next.py script for intelligent suggestions
4. Track progress in writing-progress.csv

### Phase 5: Assembly & Production
1. Create assembly instructions
2. Generate manuscript using assemble_manuscript.py
3. Add TOC and Index
4. Prepare for KDP
5. Create cover design
6. Publish!

## Using the Schema

### For Validation:
```python
import json
with open('database/database-schema.json') as f:
    schema = json.load(f)
# Use schema['fields'] to validate CSV entries
```

### For Tools:
- Field names and types are programmatically accessible
- Enumerated values can populate dropdowns
- Validation rules can enforce data quality
- Diversity targets can drive recommendation engine

### For Reference:
- Human-readable documentation is in README-DATABASE.md
- Machine-readable rules are in database-schema.json
- Both are kept in sync

## Questions to Resolve

These will be addressed as project progresses:
- Final category structure (8 categories or different grouping?)
- Entry template specifics (what sections work best for history?)
- Exact diversity targets (are 30% women / 20% BIPOC the right goals?)
- Balance between academic and popular works
- How to handle multi-volume works
- Whether to include recent (2020+) histories or focus on established classics

---

**Setup completed**: 2026-02-10
**Ready for**: Candidate collection and metadata research
**Next action**: Import candidates from comet1.md into master-candidates.csv
