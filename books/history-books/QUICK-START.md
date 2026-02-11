# History Books Quick Start Guide

## What You Have Now

✅ **41 candidates** imported from comet1.md into database/master-candidates.csv
✅ **Complete database schema** (JSON + documentation)
✅ **Project structure** ready to go
✅ **All shared scripts** work with this book

## Your Database At a Glance

**File**: `database/master-candidates.csv`

- 41 books total
- All marked as "Candidate"
- Rich metadata (24 fields per book)
- Ready to open in Excel, Google Sheets, or any CSV editor

## Major Gaps to Fill

Before selecting final 100, you need more candidates in:

### 🚨 Critical Gaps:
- **Medieval history**: 0 books (need 5-8)
- **African history**: 0 books (need 8-10)
- **Indigenous historians**: 0 authors
- **Women historians**: Only 27% (target 30%+)
- **BIPOC historians**: Only 15% (target 20%+)

### ⚠️ Important Gaps:
- **Ancient history**: Only 2 books (need 5-7 more)
- **Economic history**: Only 1 book
- **Labor history**: 0 books
- **Religious history**: Only 1 book
- **South America**: Only 2 books
- **Asia** (non-China/Japan): Limited coverage

### Current Strengths:
✅ Excellent 20th century coverage (maybe too much WWII)
✅ Strong U.S. history representation
✅ Good popular narrative books
✅ 8 Pulitzer/National Book Award winners

## Next Actions

### 1. Add More Candidates (Priority)

Get to 120-150 candidates by adding books in gap areas:

**Medieval**:
- A Distant Mirror (Barbara Tuchman)
- The Crusades Through Arab Eyes (Amin Maalouf)
- The Time Traveler's Guide to Medieval England (Ian Mortimer)

**African**:
- King Leopold's Ghost (Adam Hochschild)
- The Fate of Africa (Martin Meredith)
- Born a Crime (Trevor Noah)

**Ancient**:
- SPQR (Mary Beard)
- Persian Fire (Tom Holland)
- The Histories (Herodotus)

**Women's/Indigenous History**:
- An Indigenous Peoples' History of the United States (Roxanne Dunbar-Ortiz)
- Bury My Heart at Wounded Knee (Dee Brown)
- Hidden Figures (Margot Lee Shetterly)

See `database/IMPORT-SUMMARY.md` for detailed gap analysis and recommendations.

### 2. Open and Review Database

**Option A - Excel/LibreOffice**:
```bash
# Navigate to database
cd /home/ram/projects/100-greatest-series/books/history-books/database

# Open in your CSV editor
libreoffice master-candidates.csv
# or: open master-candidates.csv (Mac)
```

**Option B - Google Sheets** (recommended):
1. Upload `master-candidates.csv` to Google Drive
2. Open with Google Sheets
3. Use filters, sorts, pivot tables
4. Share with collaborators

### 3. Add New Candidates to CSV

**Manually**:
- Open CSV in editor
- Add new row with ID 42, 43, 44...
- Fill in fields (use schema as reference)
- Status = "Candidate"

**Or ask Claude**:
- Provide list of new candidates
- Claude can add them to CSV with metadata

### 4. Research Author Identity

For existing candidates, populate `author_identity_notes`:
- Use Wikipedia, publisher bios, official author sites
- Document source (e.g., "Wikipedia bio", "Author's website")
- Update `author_gender`, `author_person_of_color`, `author_indigenous`

### 5. Begin Selection

Once you have 120-150 candidates:
1. Filter by Tier 1 (Pulitzers, classics) → mark "Selected"
2. Check diversity balance
3. Fill geographic/temporal gaps
4. Mark tough choices as "Maybe"
5. Cut obvious rejects to "Cut"
6. Get to exactly 100 "Selected"

## Using the Scripts

All shared scripts work automatically:

```bash
cd /home/ram/projects/100-greatest-series/books/history-books

# Search for a book
python3 ../../shared/scripts/check_book.py "Guns of August"

# Get recommendations (once you have more candidates)
python3 ../../shared/scripts/recommend_next.py --limit 10

# Sync database with completed writeups (later)
python3 ../../shared/scripts/update_status.py --apply
```

## Key Files Reference

| File | Purpose |
|------|---------|
| `database/master-candidates.csv` | Main database (41 books) |
| `database/database-schema.json` | Field definitions and rules |
| `database/README-DATABASE.md` | How to use database |
| `database/IMPORT-SUMMARY.md` | Gap analysis |
| `config.yaml` | Book configuration |
| `CLAUDE.md` | Project guidance for Claude |
| This file | Quick start guide |

## Common Tasks

### Add a book manually:
1. Open `master-candidates.csv`
2. Add new row: ID 42, Status "Candidate", fill Title/Author/Year
3. Add as much metadata as you can
4. Save

### Check diversity balance:
```bash
# Count women authors
grep -c ",female," database/master-candidates.csv

# Count BIPOC authors
grep -c ",yes," database/master-candidates.csv | head -1
```

### Filter by field:
- Open in Google Sheets
- Use Data → Create a filter
- Filter by Status, Tier, era_category, etc.

### Export selected books only:
- Filter Status = "Selected"
- File → Download → CSV

## Questions?

See the full documentation:
- `database/README-DATABASE.md` - Database usage
- `CLAUDE.md` - Project overview
- `SETUP-SUMMARY.md` - What was created
- `../../shared/docs/DATABASE-SCHEMA.md` - Full schema reference

---

**Ready to go!** Start by adding more candidates to fill the gaps.
