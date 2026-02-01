# Final Canonical Layout for Book Entries

**Version:** 1.0
**Last Updated:** 2026-01-31
**Purpose:** Authoritative specification for all book entry formatting and content structure

---

## Overview

Every book entry follows a consistent two-page spread format with **exactly 8 required sections** in the order specified below. This ensures uniformity across all 100+ entries and enables automated validation and assembly.

---

## Complete Entry Structure

```markdown
# XX — [Book Title]

### *[Subtitle or Author Name]*

**"[Opening Quote]"** — *[Attribution]*

---

### **[ The Essentials ]**

* **Genre:** [Primary Genre]
* **Sub-Genre:** [Secondary Genre(s)]
* **Keywords:** *[Comma-separated keywords in italics]*
* **Traveler Profile:** **[Archetype Name].** [One-sentence description of ideal reader]

---

### **[ The Author ]** or **[ The Author: [Full Name (Birth–Death)] ]**

[Author biography: 100-150 words covering background, credentials, writing style, and why they matter to travel literature]

---

### **[ The Book ]** or **[ The Book: *[Title]* ]**

[Book description: 150-250 words covering the journey, writing quality, historical significance, and what makes this book essential. Multiple paragraphs allowed.]

---

### **[ Destinations Explored ]** or **[ Major Figures Explored ]**

[Choose ONE based on book theme:]

**For geographic travel narratives:**
* **[Location Name]:** [Evocative 1-2 sentence description]
* **[Location Name]:** [Description]
[3-6 locations typically]

**For historical/biographical works:**
* **[Person Name]:** [Role and significance]
* **[Person Name]:** [Description]
[3-6 figures typically]

---

### **[ Further Reading ]**

**By [Author Last Name]:**

* ***[Book Title]***: [One-sentence description of how it relates]
[1-3 books by same author, if available; omit section if none exist]

**In a Similar Vein:**

* ***[Book Title]*** by [Author Name]: [One-sentence description]
* ***[Book Title]*** by [Author Name]: [Description]
[2-4 related books by other authors]

---

### **[ The Signature Line ]**

> "[Defining quote from the book that captures its essence]"

---

### **[ The Perfect Pairing ]**

* **The Drink:** [Beverage that matches the book's atmosphere]
* **The Soundtrack:** [Music or sounds that evoke the journey]
* **The Setting:** [Ideal reading environment]

---
```

---

## Section-by-Section Specifications

### 1. Title Block

**Format:**
```markdown
# XX — [Book Title]

### *[Subtitle or Author Name]*

**"[Opening Quote]"** — *[Attribution]*

---
```

**Rules:**
- `XX` is a placeholder for entry number (assigned during assembly)
- Title uses single `#` heading
- Subtitle/author uses `### *italic*` format
- Opening quote must be in **bold** with attribution in *italics*
- Quote should be 1-2 sentences, memorable and evocative
- Horizontal rule (`---`) separates title block from body

---

### 2. The Essentials

**Format:**
```markdown
### **[ The Essentials ]**

* **Genre:** [Primary Genre]
* **Sub-Genre:** [Secondary Genre(s)]
* **Keywords:** *[Keywords in italics]*
* **Traveler Profile:** **[Archetype].** [Description]

---
```

**Rules:**
- Section header: `### **[ The Essentials ]**` (exact format required)
- Four required bullet points in exact order
- Keywords in italics, comma-separated (5-8 keywords typical)
- Traveler Profile has **bold archetype name** followed by description
- Common archetypes: The Solitary Seeker, The Grand Chronicler, The Cultural Observer, The Adventure Seeker, The Philosophical Wanderer
- Horizontal rule after section

**Content Guidelines:**
- Genre examples: Expedition Memoir, Narrative History, Literary Travelogue, Journalistic Reportage, Spiritual Journey
- Keywords should include: locations, themes, era markers, travel modes

---

### 3. The Author

**Format (Option A - Simple):**
```markdown
### **[ The Author ]**

[Biography paragraph]
```

**Format (Option B - With Name/Dates):**
```markdown
### **[ The Author: [Full Name (Birth–Death)] ]**

[Biography paragraph]
```

**Rules:**
- Either format is acceptable (prefer Option B for clarity)
- 100-150 words target length
- Single paragraph or multiple short paragraphs
- No horizontal rule after (flows directly into next section)

**Content Guidelines:**
- Professional background and credentials
- Why they're qualified to write this book
- Writing style and distinctive voice
- Impact on travel literature genre
- Relevant life experiences

---

### 4. The Book

**Format (Option A - Simple):**
```markdown
### **[ The Book ]**

[Description paragraphs]
```

**Format (Option B - With Title):**
```markdown
### **[ The Book: *[Title]* ]**

[Description paragraphs]
```

**Rules:**
- Either format acceptable (prefer Option B when title differs from entry title)
- 150-250 words target length
- Multiple paragraphs encouraged for readability
- Must have substantive content (minimum 50 characters after cleanup)
- Horizontal rule after section

**Content Guidelines:**
- The journey itself: where, when, how long
- Writing quality and style
- What makes it significant or unique
- Historical/cultural context
- Key themes or insights
- Why it deserves to be in the top 100

---

### 5. Destinations Explored OR Major Figures Explored

**Choose ONE based on book type:**

**Format A - Destinations (for travel narratives):**
```markdown
### **[ Destinations Explored ]**

* **[Location]:** [Description]
* **[Location]:** [Description]

---
```

**Format B - Major Figures (for historical/biographical works):**
```markdown
### **[ Major Figures Explored ]**

* **[Person]:** [Description]
* **[Person]:** [Description]

---
```

**Rules:**
- MUST have one of these two sections (validated)
- 3-6 entries typical
- Each entry: **Bold name** followed by colon and description
- Descriptions: 1-2 sentences, evocative and specific
- Horizontal rule after section

**Content Guidelines:**
- Destinations: Don't just list cities—capture the essence of each place
- Major Figures: Include role, dates if relevant, and why they matter
- Order chronologically or by importance

---

### 6. Further Reading

**Format:**
```markdown
### **[ Further Reading ]**

**By [Author Last Name]:**

* ***[Title]***: [Description]
* ***[Title]***: [Description]

**In a Similar Vein:**

* ***[Title]*** by [Author]: [Description]
* ***[Title]*** by [Author]: [Description]
* ***[Title]*** by [Author]: [Description]

---
```

**Rules:**
- Section header: `### **[ Further Reading ]**`
- Two required subsections: **"By [Author]:"** and **"In a Similar Vein:"**
- "By [Author]:" may be omitted if author has no other relevant travel books
- "In a Similar Vein:" is REQUIRED (2-4 recommendations)
- Book titles in ***bold italics***
- Horizontal rule after section

**Content Guidelines:**
- "By [Author]:" - Other travel/adventure books by same author only
- "In a Similar Vein:" - Books that pair thematically, geographically, or stylistically
- Descriptions: one sentence explaining the connection
- At least one recommendation should be from within the 100 (if applicable)

---

### 7. The Signature Line

**Format:**
```markdown
### **[ The Signature Line ]**

> "[Defining quote from the book]"
```

**Rules:**
- Section header: `### **[ The Signature Line ]**`
- Quote in blockquote format (> prefix)
- 1-2 sentences maximum
- No horizontal rule after (flows into Perfect Pairing)

**Content Guidelines:**
- The single most defining/memorable quote from the book
- Should capture the book's essence or a key insight
- Often different from opening quote (can be same if perfect)

---

### 8. The Perfect Pairing

**Format:**
```markdown
### **[ The Perfect Pairing ]**

* **The Drink:** [Beverage description]
* **The Soundtrack:** [Music or ambient sounds]
* **The Setting:** [Ideal reading environment]

---
```

**Rules:**
- Section header: `### **[ The Perfect Pairing ]**`
- Three required subsections in exact order:
  1. **The Drink:**
  2. **The Soundtrack:**
  3. **The Setting:**
- Each on its own bullet point
- Final horizontal rule to close entry

**Content Guidelines:**
- **The Drink:** Beverage that matches book's atmosphere (tea, coffee, wine, local drink from region)
- **The Soundtrack:** Music, artist/composer, or ambient sounds that evoke the journey
- **The Setting:** Where and when to read (time of day, weather, location)
- Be specific and evocative, not generic
- Connect to book's themes or geography when possible

---

## Styling Rules

### Markdown Formatting

1. **Section headers:** Always `### **[ Section Name ]**`
   - Level 3 heading (`###`)
   - Bold (`**`)
   - Square brackets (`[ ]`)
   - Exact spacing and capitalization

2. **Emphasis:**
   - ***Bold italics*** for book titles: `***Title***`
   - *Italics* for keywords, attributions: `*text*`
   - **Bold** for emphasis, names in lists: `**text**`

3. **Lists:**
   - Use `*` for bullet points (not `-` or `+`)
   - Consistent indentation (4 spaces for sub-items)

4. **Quotes:**
   - Blockquotes use `> ` prefix
   - Inline quotes use `"double quotes"`
   - Attribution with em dash: `— *Author*`

5. **Horizontal rules:**
   - Use `---` (not `***` or `___`)
   - Blank line before and after

### Content Styling

1. **Tone:**
   - Encyclopedic but engaging
   - Authoritative without being academic
   - Accessible to general readers
   - No emojis (unless explicitly requested)

2. **Length targets:**
   - The Essentials: Fixed format (4 bullets)
   - The Author: 100-150 words
   - The Book: 150-250 words
   - Total entry: 300-500 words (excluding quotes and lists)

3. **Perspective:**
   - Third person for author and book descriptions
   - Second person ("you") acceptable for Traveler Profile
   - Active voice preferred

4. **Tense:**
   - Present tense for describing book content
   - Past tense for historical events and author biography

---

## Validation Checklist

An entry is considered **complete and valid** when it has:

- ✅ Title block with opening quote (first 10 lines)
- ✅ The Essentials (with all 4 required bullets)
- ✅ The Author (with substantive content, 50+ characters)
- ✅ The Book (with substantive content, 50+ characters)
- ✅ Destinations Explored OR Major Figures Explored
- ✅ Further Reading (with "In a Similar Vein" at minimum)
- ✅ The Signature Line (with blockquote)
- ✅ The Perfect Pairing (with all 3 subsections: Drink, Soundtrack, Setting)

Use `validate_entries.py` to automatically check all entries.

---

## Special Cases

### Historical Travel Books (Pre-1800)

For very old texts like Marco Polo, Ibn Battuta, Pigafetta:
- "By [Author]:" subsection in Further Reading may be omitted (unlikely to have other travel books)
- Focus "In a Similar Vein" on other historical exploration narratives
- Major Figures Explored often more appropriate than Destinations

### Anthologies or Collections

If the book is a collection of essays/travels:
- The Book section should explain the collection's scope and structure
- Destinations/Figures can reflect the range of the collection
- Traveler Profile should address who benefits from the anthology format

### Books About Place vs. Journey

**Journey-focused books:**
- Emphasize the route, mode of travel, duration
- Destinations Explored highlights stops along the way

**Place-focused books:**
- Emphasize depth of cultural immersion
- Destinations may be a single city/region with neighborhoods/aspects as sub-items

---

## Notes for AI Tools

When generating book entries:
1. Always follow this exact structure and order
2. Use web search for accurate quotes, dates, and facts
3. Verify book titles and author names are spelled correctly
4. Match tone and style to existing entries
5. The Essentials keywords should be relevant and searchable
6. Traveler Profile should create a vivid persona
7. Perfect Pairing should be creative and specific to the book

---

## Changelog

**v1.0 (2026-01-31):**
- Initial canonical specification
- Consolidates all format variations observed in corpus
- Establishes validation requirements
- Documents special cases and exceptions
