# Starting a New Book in the 100 Greatest Series

This guide walks you through creating a new book in the series (e.g., "100 Greatest History Books").

## Quick Start (30-60 minutes)

### 1. Copy Template Structure

Start by copying an existing book's structure:

```bash
cd ~/projects/100-greatest-series/books
cp -r travel-books history-books  # or your new book name
cd history-books
```

### 2. Clean Out Book-Specific Content

Remove the previous book's content but keep the directory structure:

```bash
# Remove all entry files but keep category directories
find book-writeups -name "*.md" -type f -delete

# Clear databases (start fresh)
rm database/*.csv

# Clear output
rm -rf output/*

# Clear candidate lists
rm -rf candidate-books/*

# Optional: clear planning docs if starting from scratch
rm -rf planning/*
```

### 3. Update config.yaml

Edit `config.yaml` to define your new book:

```yaml
book:
  title: "The 100 Greatest History Books Ever Written"
  short_name: "history-books"
  target_count: 100
  output_formats: ["docx", "pdf", "epub"]

structure:
  database_dir: "database"
  writeups_dir: "book-writeups"
  assembly_dir: "assembly"
  introduction_dir: "introduction"
  output_dir: "output"

categories:
  - id: "1_ancient_world"
    name: "The Ancient World"
  - id: "2_classical_antiquity"
    name: "Classical Antiquity"
  - id: "3_medieval_period"
    name: "The Medieval Period"
  - id: "4_renaissance_enlightenment"
    name: "Renaissance and Enlightenment"
  - id: "5_modern_history"
    name: "Modern History"
  - id: "6_contemporary"
    name: "Contemporary History"

assembly:
  order_file: "assembly/Order-of-assembly.md"
  category_list_file: "assembly/final_category_list.md"

database:
  master_candidates: "database/master-candidates.csv"
  final_selection: "database/final-selection.csv"
  honorable_mentions: "database/honorable-mentions.csv"
  writing_progress: "database/writing-progress.csv"
```

### 4. Create Category Structure

Create directories for your categories:

```bash
mkdir -p book-writeups/1_ancient_world
mkdir -p book-writeups/2_classical_antiquity
mkdir -p book-writeups/3_medieval_period
mkdir -p book-writeups/4_renaissance_enlightenment
mkdir -p book-writeups/5_modern_history
mkdir -p book-writeups/6_contemporary
```

### 5. Initialize Databases

Create your database CSVs with appropriate headers. Copy the schema from `../../shared/schemas/master_candidates.schema.md` and adapt:

```bash
# Example master-candidates.csv header:
Title,Author,Year,Primary_Region,Status,Tier,Source,Notes,Theme_Category
```

Start populating with candidate books.

### 6. Update CLAUDE.md

Edit `CLAUDE.md` to reflect your new book's specifics:
- Update project description
- Update category definitions
- Update selection criteria
- Update workflow and timeline

### 7. Create Category Introductions

For each category, create `book-writeups/[category]/category_intro.md`:

```markdown
# The Ancient World

*History's earliest written records, from Mesopotamia to Rome*

The ancient world gave us our first attempts at recording the past...

---
```

### 8. Start Writing

You're ready to start! Use the shared scripts:

```bash
# Get book recommendations
python3 ../../shared/scripts/recommend_next.py

# Check database
python3 ../../shared/scripts/check_book.py "Herodotus"

# Assemble manuscript
python3 ../../shared/scripts/assemble_manuscript.py
```

## Category System Design

When designing your category system, consider:

### Good Category Systems
- **Thematic**: Group by subject (ancient, medieval, modern)
- **Geographic**: Group by region (Europe, Asia, Americas)
- **Methodological**: Group by approach (social history, military history, cultural history)
- **Chronological**: Group by time period

### Category Guidelines
- **5-10 categories** works well for 100 books
- **10-15 books per category** maintains balance
- **Clear distinctions** - books shouldn't fit multiple categories equally
- **Narrative flow** - categories should tell a story when read in order

## Database Schema

Essential fields for any book:
- **Title**: Full book title
- **Author**: Author name
- **Year**: Publication year
- **Status**: Candidate | Selected | Completed | Rejected
- **Tier**: 1-4 (importance/popularity ranking)
- **Theme_Category**: Which category this belongs to

Optional but recommended:
- **Primary_Region**: Geographic focus
- **Genre**: Book style (narrative, academic, biography, etc.)
- **Notes**: Research notes
- **Source**: Where you found this candidate

## Entry Template

Adapt the template from `../../shared/templates/TEMPLATE.md` to your book's needs. The travel books template has:
- Title & memorable quote
- The Essentials (genre, keywords)
- The Author (biographical sketch)
- The Book (significance, what makes it great)
- Further Reading
- The Signature Line
- The Perfect Pairing

You might adapt this for history books as:
- Title & historical context
- The Essentials
- The Historian
- The History (period covered, approach, significance)
- Further Reading
- Key Arguments/Themes

## Testing Your Setup

Once configured, test the scripts:

```bash
# Test path detection
python3 ../../shared/scripts/book_utils.py

# Test database loading
python3 ../../shared/scripts/check_book.py "test"

# Test manuscript assembly (will fail if no entries yet, but checks config)
python3 ../../shared/scripts/assemble_manuscript.py
```

## Workflow

1. **Research phase** (1-2 weeks)
   - Identify 150-200 candidate books
   - Populate database
   - Define tier rankings

2. **Selection phase** (1 week)
   - Use recommend_next.py to prioritize
   - Narrow to final 100
   - Ensure category balance

3. **Writing phase** (3-4 weeks)
   - Write entries in batches
   - Use update_status.py to track progress
   - Aim for 5-10 entries per day

4. **Assembly phase** (1 week)
   - Run assemble_manuscript.py
   - Review and edit
   - Create front/back matter
   - Generate PDF and EPUB

## Tips

- **Start with tier 1 books** - The well-known ones are easier to write
- **Batch by category** - Write all books in one category together
- **Research efficiently** - Use WebSearch for facts, read reviews not full books
- **Maintain voice** - Keep style consistent with series tone
- **Track progress** - Use recommend_next.py regularly to see gaps

## Common Issues

### "No module named 'yaml'"
Install PyYAML: `pip install pyyaml`

### "Could not find config.yaml"
Make sure you're running scripts from within the book directory, or use `--book-root` parameter

### "FileNotFoundError: output directory"
The script should create it automatically, but you can manually: `mkdir output`

### Script can't find books
Check that:
1. Category directories exist in `book-writeups/`
2. Category IDs in config.yaml match directory names
3. Files are named correctly (lowercase, hyphens, .md extension)

## Questions?

See the main series README at `../../README.md` or check existing book projects for examples.
