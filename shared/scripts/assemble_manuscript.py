#!/usr/bin/env python3
"""
Assemble the 100 Travel Books manuscript from markdown files into a Word document.
Numbers books sequentially from 01-101 during assembly.
"""

import re
import argparse
from pathlib import Path
from datetime import datetime
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from book_utils import find_book_root, load_config, get_book_path


def add_hyperlink(paragraph, text, url):
    """
    Add a hyperlink to a paragraph.
    """
    part = paragraph.part
    r_id = part.relate_to(url, 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink', is_external=True)

    hyperlink = OxmlElement('w:hyperlink')
    hyperlink.set(qn('r:id'), r_id)

    new_run = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')

    # Set hyperlink styling
    c = OxmlElement('w:color')
    c.set(qn('w:val'), '0563C1')
    rPr.append(c)

    u = OxmlElement('w:u')
    u.set(qn('w:val'), 'single')
    rPr.append(u)

    new_run.append(rPr)
    new_run.text = text
    hyperlink.append(new_run)

    paragraph._p.append(hyperlink)
    return hyperlink


def clean_heading_text(text):
    """
    Remove markdown formatting from heading text.
    Removes: **, *, [ and ]
    """
    # Remove bold markers
    text = text.replace('**', '')
    # Remove italic markers (but be careful not to remove asterisks from bullet points)
    text = re.sub(r'(?<!\*)\*(?!\*)', '', text)
    # Remove square brackets
    text = text.replace('[', '').replace(']', '')
    # Clean up extra spaces
    text = ' '.join(text.split())
    return text.strip()


def parse_inline_formatting(text, paragraph):
    """
    Parse inline markdown formatting (bold, italic, links) and add to paragraph.
    """
    if not text:
        return

    # Pattern to match **bold**, *italic*, and [text](url)
    pattern = r'(\*\*.*?\*\*|\*.*?\*|\[.*?\]\(.*?\))'
    parts = re.split(pattern, text)

    for part in parts:
        if not part:
            continue

        if part.startswith('**') and part.endswith('**'):
            # Bold text
            run = paragraph.add_run(part[2:-2])
            run.bold = True
        elif part.startswith('*') and part.endswith('*') and not part.startswith('**'):
            # Italic text
            run = paragraph.add_run(part[1:-1])
            run.italic = True
        elif part.startswith('[') and '](' in part:
            # Hyperlink
            match = re.match(r'\[(.*?)\]\((.*?)\)', part)
            if match:
                link_text = match.group(1)
                url = match.group(2)
                add_hyperlink(paragraph, link_text, url)
        else:
            # Regular text
            paragraph.add_run(part)


def replace_book_number(content, book_number):
    """
    Replace XX or existing numbers with the actual book number in the content.
    Looks for patterns like "# XX —", "# 52 —", "**# [Entry Number] —", etc.
    """
    # Format number as zero-padded (01, 02, ..., 101)
    num_str = str(book_number).zfill(2)

    # Replace various patterns
    patterns = [
        (r'^#\s+XX\s+—', f'# {num_str} —'),  # # XX —
        (r'^#\s+\d+\s+—', f'# {num_str} —'),  # # 52 —
        (r'^#\s+XX\s*:', f'# {num_str}:'),    # # XX:
        (r'^#\s+\d+\s*:', f'# {num_str}:'),   # # 52:
        (r'^\*\*#\s+\[Entry Number\]\s+—', f'# {num_str} —'),  # **# [Entry Number] —
    ]

    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)

    return content


def parse_book_entry(md_content):
    """
    Parse a book entry markdown and extract key sections.
    Returns a dict with: title, author_name, author_quote, signature_quote, and sections
    """
    lines = md_content.split('\n')

    entry = {
        'title': '',
        'author_name': '',
        'author_quote': '',
        'signature_quote': '',
        'sections': {}  # Will hold sections like 'essentials', 'author_bio', etc.
    }

    current_section = None
    current_content = []
    in_signature_section = False

    for i, line in enumerate(lines):
        line_stripped = line.strip()

        # Skip empty lines and separators at the start
        if not line_stripped or line_stripped == '---':
            continue

        # Extract title (first heading level 1)
        if line_stripped.startswith('# ') and not entry['title']:
            entry['title'] = clean_heading_text(line_stripped[2:])
            continue

        # Extract author name (heading level 3 starting with "By" or just after title)
        if line_stripped.startswith('### ') and line_stripped.startswith('### *By '):
            entry['author_name'] = clean_heading_text(line_stripped[4:].replace('*By ', '').replace('*', ''))
            continue

        # Extract author quote (the quote near the top with author attribution)
        if line_stripped.startswith('**"') and '—' in line_stripped and not entry['author_quote']:
            entry['author_quote'] = line_stripped
            continue

        # Detect signature line section
        if 'Signature Line' in line_stripped and line_stripped.startswith('###'):
            in_signature_section = True
            current_section = None
            continue

        # Extract signature quote (blockquote in signature section)
        if in_signature_section and line_stripped.startswith('>'):
            entry['signature_quote'] = line_stripped.lstrip('> ').strip()
            in_signature_section = False
            continue

        # Detect section headers (Heading 3)
        if line_stripped.startswith('### '):
            # Save previous section
            if current_section and current_content:
                entry['sections'][current_section] = '\n'.join(current_content).strip()
                current_content = []

            # Start new section
            section_title = clean_heading_text(line_stripped[4:])

            # Map section titles to keys
            if 'Essentials' in section_title:
                current_section = 'essentials'
            elif 'The Author:' in section_title or section_title.startswith('The Author'):
                current_section = 'author_bio'
                # Extract author name from "The Author: Name (years)" if present
                match = re.search(r'The Author:\s*(.+)', section_title)
                if match and not entry['author_name']:
                    entry['author_name'] = match.group(1).strip()
            elif 'The Book' in section_title:
                current_section = 'the_book'
            elif 'Destinations' in section_title:
                current_section = 'destinations'
            elif 'Further Reading' in section_title:
                current_section = 'further_reading'
            elif 'Perfect Pairing' in section_title:
                current_section = 'perfect_pairing'
            else:
                current_section = section_title.lower().replace(' ', '_')

            continue

        # Collect content for current section
        if current_section:
            current_content.append(line)

    # Save last section
    if current_section and current_content:
        entry['sections'][current_section] = '\n'.join(current_content).strip()

    return entry


def add_book_entry_to_doc(doc, entry):
    """
    Add a structured book entry to the document following the specified order.
    """
    # 1. Book Title (Heading 1)
    if entry['title']:
        para = doc.add_heading(entry['title'], level=1)
        para.runs[0].font.size = Pt(20)
        para.runs[0].font.bold = True

    # 2. Author Name (Heading 2)
    if entry['author_name']:
        para = doc.add_heading(entry['author_name'], level=2)
        para.runs[0].font.size = Pt(16)
        para.runs[0].font.bold = True

    # 3. Signature Line Quote (centered, no label)
    if entry['signature_quote']:
        para = doc.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = para.add_run(f'"{entry["signature_quote"]}"')
        run.italic = True
        run.font.size = Pt(12)

    # 4. The Essentials (Heading 3)
    if 'essentials' in entry['sections']:
        para = doc.add_heading('The Essentials', level=3)
        para.runs[0].font.size = Pt(14)
        add_markdown_to_doc(doc, entry['sections']['essentials'])

    # 5. The Author (Heading 3) - biographical section
    if 'author_bio' in entry['sections']:
        para = doc.add_heading('The Author', level=3)
        para.runs[0].font.size = Pt(14)
        add_markdown_to_doc(doc, entry['sections']['author_bio'])

    # 6. Author Quote (below the biographical section)
    if entry['author_quote']:
        para = doc.add_paragraph()
        parse_inline_formatting(entry['author_quote'], para)
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in para.runs:
            run.font.size = Pt(11)

    # 7. The Book (Heading 3)
    if 'the_book' in entry['sections']:
        para = doc.add_heading('The Book', level=3)
        para.runs[0].font.size = Pt(14)
        add_markdown_to_doc(doc, entry['sections']['the_book'])

    # 8. Destinations Explored (Heading 3)
    if 'destinations' in entry['sections']:
        para = doc.add_heading('Destinations Explored', level=3)
        para.runs[0].font.size = Pt(14)
        add_markdown_to_doc(doc, entry['sections']['destinations'])

    # 9. Further Reading (Heading 3)
    if 'further_reading' in entry['sections']:
        para = doc.add_heading('Further Reading', level=3)
        para.runs[0].font.size = Pt(14)
        add_markdown_to_doc(doc, entry['sections']['further_reading'])

    # 10. The Perfect Pairing (Heading 3)
    if 'perfect_pairing' in entry['sections']:
        para = doc.add_heading('The Perfect Pairing', level=3)
        para.runs[0].font.size = Pt(14)
        add_markdown_to_doc(doc, entry['sections']['perfect_pairing'])


def add_markdown_to_doc(doc, md_content):
    """
    Parse markdown content and add it to the Word document with appropriate formatting.
    """
    lines = md_content.split('\n')
    i = 0

    while i < len(lines):
        line = lines[i].rstrip()

        # Skip empty lines at the start
        if not line:
            i += 1
            continue

        # Headers (shouldn't appear here in book entries, but keep for other content)
        if line.startswith('#'):
            level = len(line) - len(line.lstrip('#'))
            text = clean_heading_text(line.lstrip('#').strip())

            if level == 1:
                para = doc.add_heading(text, level=1)
                para.runs[0].font.size = Pt(24)
                para.runs[0].font.bold = True
            elif level == 2:
                para = doc.add_heading(text, level=2)
                para.runs[0].font.size = Pt(18)
                para.runs[0].font.bold = True
            elif level == 3:
                para = doc.add_heading(text, level=3)
                para.runs[0].font.size = Pt(14)
                para.runs[0].font.bold = True
            else:
                para = doc.add_heading(text, level=4)
                para.runs[0].font.size = Pt(12)
                para.runs[0].font.bold = True

        # Horizontal rules
        elif line.strip() == '---':
            para = doc.add_paragraph()
            para.add_run('___________________________________________')
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Block quotes
        elif line.startswith('>'):
            quote_text = line.lstrip('>').strip()
            para = doc.add_paragraph()
            para.style = 'Quote'
            parse_inline_formatting(quote_text, para)
            para_format = para.paragraph_format
            para_format.left_indent = Inches(0.5)
            para_format.right_indent = Inches(0.5)
            for run in para.runs:
                run.italic = True

        # Bullet lists
        elif line.startswith('* ') or line.startswith('- '):
            text = line[2:].strip()
            para = doc.add_paragraph(style='List Bullet')
            parse_inline_formatting(text, para)

        # Numbered lists
        elif re.match(r'^\d+\.\s', line):
            text = re.sub(r'^\d+\.\s+', '', line)
            para = doc.add_paragraph(style='List Number')
            parse_inline_formatting(text, para)

        # Regular paragraphs
        else:
            para = doc.add_paragraph()
            parse_inline_formatting(line, para)

        i += 1


def get_book_order():
    """
    Return the ordered list of books by category in chronological order.
    Now includes 101 books total.
    """
    order = {
        '1_first_routes': [
            'the-travels-marco-polo.md',              # 1300
            'the-rihla-ibn-battuta.md',               # 1355
            'the-first-voyage-antonio-pigafetta.md',  # 1525
            'journey-to-western-islands-johnson.md',  # 1775
            'personal-narrative-von-humboldt.md',     # 1814
            'voyage-of-the-beagle-darwin.md',         # 1839
            'incidents-of-travel-in-yucatan-stephens.md', # 1843
            'oregon-trail-parkman.md',                # 1849
            'travels-in-west-africa-mary-kingsley.md', # 1897
            'sailing-alone-joshua-slocum.md',         # 1900
            'blue-nile-moorehead.md'                  # 1962
        ],
        '2_exploration': [
            'south-ernest-shackleton.md',             # 1919
            'worst-journey-cherry-garrard.md',        # 1922
            'libyan-sands-ralph-bagnold.md',          # 1935
            'cruel-way-ella-maillart.md',             # 1947
            'arabian-sands-thesiger.md',              # 1959
            'coming-into-the-country-john-mcphee.md', # 1977
            'snow-leopard-matthiessen.md',            # 1978
            'tracks-robyn-davidson.md',               # 1980
            'arctic-dreams-barry-lopez.md',           # 1986
            'maiden-voyage-tanya-aebi.md',            # 1989
            'terra-incognita-sara-wheeler.md',        # 1996 - EXTRA
            'into-the-wild-krakauer.md',              # 1996
            'cruelest-journey-kira-salak.md'          # 2004
        ],
        '3_slow_routes': [
            'the-narrow-road-basho.md',               # 1689 - EXTRA
            'travels-with-a-donkey-stevenson.md',     # 1879
            'path-to-rome-belloc.md',                 # 1902
            'man-who-walked-colin-fletcher.md',       # 1968
            'as-i-walked-out-lee.md',                 # 1969
            'a-time-of-gifts-fermor.md',              # 1977
            'roads-to-sata-booth.md',                 # 1985
            'chasing-the-monsoon-frater.md',          # 1990
            'roads-to-santiago-nooteboom.md',         # 1992
            'old-ways-macfarlane.md',                 # 2012
            'walking-with-abel-badkhen.md',           # 2015
            'salt-path-raynor-winn.md'                # 2018
        ],
        '4_frontiers': [
            'turkish-embassy-letters-montagu.md',     # 1763
            'ride-to-khiva-fred-burnaby.md',          # 1876
            'unbeaten-tracks-isabella-bird.md',       # 1880
            'travels-in-arabia-deserta-doughty.md',   # 1888
            'my-journey-to-lhasa-davidneel.md',       # 1927
            'valley-of-the-assasins.md',              # 1934
            'road-to-tartary-fleming.md',             # 1935 (News from Tartary)
            'road-to-oxiana-byron.md',                # 1937
            'in-an-antique-land-ghosh.md',            # 1992
            'from-holy-mountain-dalrymple.md',        # 1997
            'unexpected-light-jason-elliott.md',      # 1999
            'travels-with-a-tangerine-mackintosh-smith.md', # 2001
            'great-hedge-of-india-moxham.md',         # 2001
            'places-in-between-rory-stewart.md'       # 2006
        ],
        '5_humbled': [
            'short-walk-down-hindu-kush-newby.md',    # 1958
            'from-heaven-lake-vikram-seth.md',        # 1983
            'great-american-bus-adler.md',            # 1986
            'video-night-pico-iyer.md',               # 1988
            'walk-in-the-woods-bryson.md',            # 1998
            'dark-continent-khumalo.md',              # 2007
            'turn-right-at-machu-adams.md'            # 2011
        ],
        '6_institutional': [
            'way-of-the-world-bouvier.md',            # 1963
            'full-tilt-devla-murphy.md',              # 1965
            'great-railway-bazaar-theroux.md',        # 1975
            'jupiters-travels-ted-simon.md',          # 1979 - EXTRA
            'blue-highways-heat-moon.md',             # 1982
            'into-the-heart-of-borneo-ohanlon.md',    # 1984
            'motoring-with-md-eric-hansen.md',        # 1991
            'river-center-world-winchester.md',       # 1996
            'fortune-teller-told-terzani.md',         # 1997
            'passage-to-juneau-raban.md',             # 1999
            'shadow-of-silk-road.md',                 # 2006
            'first-overland-tim-slessor.md'           # 2006
        ],
        '7_inhabited_landscapes': [
            'house-in-bali-mcphee.md',                # 1946
            'pattern-of-islands-grimble.md',          # 1952
            'windward-road-archie-carr.md',           # 1956
            'venice-jan-morris.md',                   # 1960
            'cities-and-stones-aldiss.md',            # 1966
            'iron-and-silk-salzman.md',               # 1986
            'year-in-provence-peter-mayle.md',        # 1989
            'river-town-hessler.md',                  # 2001
            'maximum-city-mehta.md',                  # 2004
            'indonesia-etc-pisani.md'                 # 2014
        ],
        '8_political': [
            'black-lamb-rebecca-west.md',             # 1941
            'naples-44-norman-lewis.md',              # 1978
            'africa-calliope-hoagland.md',            # 1979
            'small-place-jamaica-kincaid.md',         # 1988
            'great-game-peter-hopkirk.md',            # 1990
            'my-traitors-heart-malan.md',             # 1990
            'shadow-of-sun-kapuscinski.md',           # 2001
            'when-crocodile-godwin.md',               # 2006
            'blood-river-tim-butcher.md',             # 2008
            'wild-coast-john-gimlette.md',            # 2011
            'border-kapka-kassova.md'                 # 2017
        ],
        '9_self_reckoning': [
            'west-with-the-night-markham.md',         # 1942
            'travels-with-charley-steinbeck.md',      # 1962
            'area-of-darkness-naipaul.md',            # 1964
            'in-patagonia-chatwin.md',                # 1977
            'travels-with-myself-gellhorn.md',        # 1978
            'there-and-then-thubron.md',              # 1992 (James Salter)
            'motorcyle-diaries-guevara.md',           # 1993
            'out-of-sheer-rage-dyer.md',              # 1997
            'catfish-and-mandala-pham.md',            # 1999
            'one-day-i-will-write-wainaina.md',       # 2011
            'looking-for-transwonderland-sarowiwa.md' # 2012
        ]
    }
    return order


def main():
    """
    Main function to assemble the manuscript.
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Assemble book manuscript from markdown files')
    parser.add_argument('--book-root', type=str, help='Path to book root directory (auto-detected if not provided)')
    args = parser.parse_args()

    # Find book root and load config
    if args.book_root:
        base_path = Path(args.book_root).resolve()
    else:
        base_path = find_book_root()

    config = load_config(base_path)
    book_title = config['book']['short_name']
    categories_config = config['categories']

    print(f"Book root: {base_path}")
    print(f"Book: {config['book']['title']}")

    # Create a new Word document
    doc = Document()

    # Set default font
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Georgia'
    font.size = Pt(11)

    print("\nStarting manuscript assembly...")

    # 1. Add Preface
    print("Adding preface...")
    intro_path = get_book_path(base_path, 'introduction_dir')
    preface_path = intro_path / 'preface_unified.md'
    if preface_path.exists():
        with open(preface_path, 'r', encoding='utf-8') as f:
            add_markdown_to_doc(doc, f.read())
        doc.add_page_break()
    else:
        print(f"Warning: {preface_path} not found")

    # 2. Add Organizing Principle Essay
    print("Adding organizing principle essay...")
    org_principle_path = intro_path / 'organizing_principle_essay.md'
    if org_principle_path.exists():
        with open(org_principle_path, 'r', encoding='utf-8') as f:
            add_markdown_to_doc(doc, f.read())
        doc.add_page_break()
    else:
        print(f"Warning: {org_principle_path} not found")

    # 3. Process each category
    book_order = get_book_order()
    categories = [cat['id'] for cat in categories_config]

    book_number = 1  # Start numbering from 1
    writeups_path = get_book_path(base_path, 'writeups_dir')

    for category in categories:
        print(f"\nProcessing category: {category}")
        category_path = writeups_path / category

        # Add page break before category introduction
        doc.add_page_break()

        # Add category introduction
        category_intro_path = category_path / 'category_intro.md'
        if category_intro_path.exists():
            print(f"  Adding category intro...")
            with open(category_intro_path, 'r', encoding='utf-8') as f:
                add_markdown_to_doc(doc, f.read())
        else:
            print(f"  Warning: {category_intro_path} not found")

        # Add each book in chronological order
        if category in book_order:
            for book_file in book_order[category]:
                book_path = category_path / book_file
                if book_path.exists():
                    print(f"  Adding book #{book_number:02d}: {book_file}")

                    # Add page break before each book entry
                    doc.add_page_break()

                    with open(book_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Replace XX or existing number with current book number
                        content = replace_book_number(content, book_number)
                        # Parse book entry and add to document
                        entry = parse_book_entry(content)
                        add_book_entry_to_doc(doc, entry)

                    book_number += 1
                else:
                    print(f"  Warning: {book_path} not found")

    # Save the document with timestamp
    output_dir = get_book_path(base_path, 'output_dir')
    output_dir.mkdir(parents=True, exist_ok=True)  # Ensure output directory exists

    # Generate timestamp filename
    timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M')
    output_path = output_dir / f'{book_title}-manuscript-{timestamp}.docx'

    doc.save(output_path)
    print(f"\n✓ Manuscript saved to: {output_path}")
    print(f"✓ Total books numbered: {book_number - 1}")
    print("Done!")


if __name__ == '__main__':
    main()
