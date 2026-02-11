# Database Files Guide - History Books

## Files in this directory

### database-schema.json
**Machine-readable schema definition** with complete field specifications:
- Field names, types, and validation rules
- Enumerated values for dropdown fields
- Diversity targets and workflow guidance
- Use this for validation and tool development

### master-candidates.csv
**Complete list of candidate history books** with essential metadata:
- All candidates from various sources (AI recommendations, awards lists, personal reading)
- Consolidated and de-duplicated
- Status: All marked as "Candidate" initially
- Source tracking shows where each book came from

**Core Fields:**
- **ID** (1-200) - Unique identifier
- **Status** - Candidate / Selected / HonorableMention / Cut / Completed
- **Title** - Full book title
- **Author** - Author's full name
- **author_gender** - Values: `male`, `female`, `nonbinary`, `unknown` (default: unknown)
- **author_indigenous** - Values: `yes`, `no`, `unknown` (default: unknown)
- **author_person_of_color** - Values: `yes`, `no`, `unknown` (default: unknown)
- **author_identity_notes** - Source for identity info (e.g., "Wikipedia bio")
- **Year** - Publication year (first edition)
- **time_period_covered** - Historical period (e.g., "1914-1918", "Ancient Rome 27 BC - 476 AD")
- **era_category** - Broad era: Ancient / Medieval / Early Modern / 19th Century / 20th Century / 21st Century / Multiple Eras / Thematic
- **geographic_scope** - Pipe-separated regions (e.g., "Europe|Asia")
- **Primary_Region** - Main geographic focus
- **history_type** - Type(s): Military / Political / Social / Cultural / Economic / etc. (pipe-separated)
- **narrative_style** - Academic / Popular Narrative / Microhistory / Biography / etc.
- **historiographical_approach** - Scholarly approach or school
- **primary_sources** - yes / no / mixed / unknown
- **Tier** - 1-4 quality system
- **awards** - Major awards (Pulitzer, National Book Award, etc.)
- **reader_archetype** - Who this book is for
- **page_count** - Approximate length
- **accessibility** - Easy / Moderate / Challenging / Very Challenging
- **Source** - Where you found this candidate
- **Notes** - Additional information

### How to use:

**Option 1: Local CSV editing**
- Open in Excel, LibreOffice, Numbers, or VS Code
- Sort and filter as needed
- Change Status column to "Selected" for final 100
- Change Status to "Cut" for eliminated books
- Use "HonorableMention" for near-misses

**Option 2: Google Sheets (recommended for collaboration)**
- Upload to Google Drive
- Import as Google Sheet
- Enables filtering, sorting, comments, formulas
- Can share with collaborators if needed

## Selection Process

### Step 1: Quick First Pass
Sort by Tier and mark obvious includes:
- Tier 1 Pulitzer/award winners you want → "Selected"
- Tier 4 wildcards you're unsure about → maybe mark "Unlikely"
- Books you know you don't want → "Cut"

### Step 2: Balance Check
Filter by Status = "Selected" and check:
- **Geographic distribution**: Use geographic_scope column
  - Not too Euro/US-centric
  - Include Africa, Asia, Latin America, Middle East
- **Era mix**: Use era_category
  - Not dominated by WWII or 20th century
  - Include ancient, medieval, early modern
- **History type diversity**: Use history_type
  - Not all military or political
  - Include social, cultural, economic, biographical
- **Author diversity**:
  - Use author_gender column (target: 30%+ female)
  - Use author_person_of_color column (target: 20%+ yes)
  - Use author_indigenous column (include indigenous historians)
- **Accessibility mix**: Use accessibility column
  - Not all academic or all popular
  - Balance between accessible and challenging

### Step 3: Fill Gaps
Based on what's missing, select from remaining candidates:
- Need more women? Filter by author_gender = "female"
- Need more ancient history? Filter by era_category = "Ancient"
- Need more non-Western perspectives? Filter by geographic_scope
- Need more accessible books? Filter by accessibility = "Easy" or "Moderate"

### Step 4: Final Cuts
When you have ~110-120 "Selected":
- Make hard choices between similar books
- Consider: Do we need 3 WWII books? Or just 2?
- Eliminate overlapping topics (e.g., multiple French Revolution books)
- Get to exactly 100

## Populating Author Identity Fields

The author identity columns (author_gender, author_indigenous, author_person_of_color) currently default to "unknown". Populate these fields using:

**Priority 1: Well-known authors**
- Research from Wikipedia, publisher pages, official bios
- Document source in author_identity_notes
- Examples: Barbara Tuchman (female), W.E.B. Du Bois (person of color)

**Priority 2: Selected books**
- Research authors of books marked "Selected"
- Use reliable biographical sources
- Note source in author_identity_notes field

**Priority 3: Remaining candidates**
- Leave as "unknown" until research phase
- Research systematically during selection process

**Best Practices:**
- Always cite your source in author_identity_notes
- Use "unknown" rather than guessing
- Be respectful and use author's self-identification when available
- For historical figures, use established biographical sources

## History-Specific Considerations

### Time Period Coverage
- **Ancient (pre-500 CE)**: Greece, Rome, Egypt, China, etc.
- **Medieval (500-1500)**: Crusades, feudalism, Islamic Golden Age
- **Early Modern (1500-1800)**: Renaissance, Reformation, Age of Exploration
- **19th Century**: Industrialization, nationalism, colonialism
- **20th Century**: World Wars, Cold War, decolonization
- **21st Century**: Recent history, contemporary analysis
- **Thematic**: Books spanning multiple eras (e.g., history of capitalism)

### History Types
Balance across:
- **Military**: Wars, battles, military strategy
- **Political**: Governments, revolutions, leaders
- **Social**: Daily life, class, family structures
- **Cultural**: Ideas, art, religion, science
- **Economic**: Trade, capitalism, labor
- **Biographical**: Lives of historical figures
- **Environmental**: Climate, geography's role in history
- **Women's History**: Often overlooked perspectives
- **Colonial/Imperial**: Empire, colonization, resistance

### Narrative Styles
Consider mix of:
- **Academic**: Original research, footnoted, for specialists
- **Popular Narrative**: Storytelling approach, accessible
- **Microhistory**: Deep dive into small event revealing larger patterns
- **Biography**: Life story illuminating era
- **Synthesis/Survey**: Big picture, broad scope

## Quality Tiers

**Tier 1: Defining Works (expect ~25-30 books)**
- Pulitzer Prize winners
- National Book Award winners
- Household names (Guns of August, People's History of United States)
- Books that defined how we see a period

**Tier 2: Essential Reading (expect ~35-40 books)**
- Widely cited in academic contexts
- Essential for understanding major topics
- Strong scholarly reputation
- Well-reviewed, influential

**Tier 3: Deep Dives (expect ~20-25 books)**
- Specialist favorites
- Important but narrower focus
- Academic reputation but less mainstream
- Intellectually demanding

**Tier 4: Wildcards (expect ~10-15 books)**
- Newer works not yet canonical
- Niche topics worth including
- Controversial but important perspectives
- Hidden gems

## Next Steps

1. **Import existing candidates** from comet1.md or other sources
2. **Add basic metadata** for each candidate (Title, Author, Year, Tier)
3. **Research identity fields** for known authors
4. **Start selection process** - mark obvious "Selected" choices
5. **Check balance** using filters and pivot tables
6. **Fill gaps** based on diversity analysis
7. **Get to final 100** - then begin writing!

## Additional Files to Create

As you progress, create these additional CSV files:

- **final-selection.csv** - Copy of Selected books only (100 entries)
- **honorable-mentions.csv** - Near-misses worth mentioning
- **writing-progress.csv** - Track completion of writeups

---

**Last Updated:** 2026-02-10

**Schema Version:** 1.0

See `database-schema.json` for complete field definitions and validation rules.
