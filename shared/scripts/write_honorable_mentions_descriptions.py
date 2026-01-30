#!/usr/bin/env python3
"""
Write proper one-line descriptions for all honorable mentions
"""

import csv
from pathlib import Path
from collections import defaultdict
from book_utils import find_book_root, load_config, get_book_path

# Hand-crafted one-line descriptions for each book (20-30 words)
descriptions = {
    # Category I: First Routes and Foundational Journeys
    "Around the World on a Bicycle": "The first person to circle the globe on two wheels, crossing continents in the 1880s before paved roads existed.",
    "The Journal of a Tour to the Hebrides": "Samuel Johnson and James Boswell's 18th-century ramble through the Scottish islands, capturing Highland life before the modern world arrived.",
    "The Journals of Captain Cook": "The legendary navigator's firsthand logs from his Pacific voyages, discovering new lands and mapping the world's final blank spaces.",
    "The Last Grain Race": "A teenager joins the last commercial sailing ship to round Cape Horn, catching the final days of the great age of sail.",
    "Balkan Ghosts": "Traveling through Yugoslavia as it fragments into war, tracing centuries of ethnic tension and history repeating itself in the Balkans.",

    # Category II: Exploration at the Edge
    "A Traveller on Horseback": "A woman rides solo through Turkey and Iran in the 1980s, navigating mountains, hospitality, and a male-dominated landscape on horseback.",
    "Brazilian Adventure": "Peter Fleming's comic misadventure searching for a lost explorer in the Amazon, proving that not all expeditions need succeed to entertain.",
    "Eiger Dreams": "Jon Krakauer's early essays on obsession and death in the mountains, profiling climbers who risk everything for one more summit.",
    "Into Thin Air": "The deadliest day on Everest: a journalist's harrowing firsthand account of the 1996 disaster that killed eight climbers in a single storm.",
    "Kon-Tiki": "Norwegian explorer crosses 5,000 miles of Pacific on a balsa raft to prove Polynesia could have been settled from South America.",
    "Lost in Shangri-La": "A World War II plane crash in New Guinea drops survivors into a Stone Age valley untouched by the modern world.",
    "Running the Amazon": "The first person to walk the Amazon's entire length, from Peruvian glaciers to the Atlantic—860 days through jungle, mountains, and madness.",
    "Stranger in the Forest": "Walking across Borneo's interior through headhunter territory, relying on rainforest tribes for food, shelter, and safe passage through the wild.",
    "Tiger of the Snows": "Tenzing Norgay's own story of conquering Everest, told from the Sherpa perspective often overshadowed by Edmund Hillary's fame.",

    # Category III: Slow Routes and Long Ways Through
    "A Walk Across America": "A disillusioned graduate walks from New York to Oregon with his dog, discovering small-town kindness and rediscovering America's heart.",
    "On Foot to the Golden Horn": "Walking from Poland to Istanbul through post-Cold War Eastern Europe, tracing Ottoman history as communism's ghosts still linger.",
    "Walking the Amazon": "British explorer becomes first person to walk the Amazon River's full length—28 months battling jungle, illness, and near-madness in isolation.",

    # Category IV: Frontiers and Frictions
    "Bitter Lemons of Cyprus": "Lawrence Durrell's bittersweet memoir of 1950s Cyprus, watching the island descend into violence between Greek and Turkish communities during British rule.",
    "In the Empire of Genghis Khan": "On horseback across Mongolia, following ancient trade routes and living with nomads whose way of life mirrors the great Khan's era.",
    "Beyond the Sky and the Earth": "A Canadian teacher spends eight years in remote Bhutan, one of the world's most isolated kingdoms, finding love and transformation.",

    # Category V: Humbled by the World
    "At the Tomb of the Inflatable Pig": "Wandering through Paraguay, South America's forgotten country, uncovering bizarre dictators, utopian colonies, and a nation time forgot.",
    "In a Sunburned Country": "Bill Bryson's hilarious journey through Australia, a continent trying to kill you with sharks, spiders, jellyfish, and exceptional friendliness.",
    "The Innocents Abroad": "Mark Twain's satirical steamship tour of Europe and the Holy Land, skewering American tourists and Old World pretensions with sharp wit.",
    "The Lost Continent": "Bill Bryson searches for the perfect American small town, finding mall sprawl, nostalgia, and the gap between Norman Rockwell dreams and reality.",
    "Notes from a Small Island": "Bryson's affectionate farewell to Britain after 20 years, celebrating eccentricity, warm beer, and a nation of apologetic queue-lovers before moving home.",

    # Category VI: Institutional Constraints
    "Dark Star Safari": "Paul Theroux returns to Africa 40 years later, traveling overland from Cairo to Cape Town through failing states and broken promises.",
    "The Lunatic Express": "Journalist rides the world's most dangerous transport—overloaded ferries, cliff-edge buses, and trains held together by prayer in the developing world.",
    "Ghost Train to the Eastern Star": "Thirty years after The Great Railway Bazaar, Paul Theroux retraces his rails through a transformed Asia, measuring change and loss.",

    # Category VII: Inhabited Landscapes
    "City of Djinns": "William Dalrymple's year in Delhi, peeling back layers of Mughal splendor, Partition trauma, and modern chaos in India's ancient capital.",
    "Flame Trees of Thika": "A child's memoir of growing up on a Kenyan coffee farm in colonial East Africa, just before World War I changed everything.",
    "Somebody's Heart is Burning": "A woman's transformative journey through West Africa, discovering stories of resilience, friendship, and unexpected connection across cultural divides.",
    "Tell My Horse": "Zora Neale Hurston explores Haiti and Jamaica's voodoo practices, documenting Caribbean folklore and spiritual traditions as both anthropologist and storyteller.",
    "The Outrun": "Returning to Scotland's Orkney Islands to recover from addiction, finding healing in wild landscapes, birds, and the rhythm of island life.",
    "The Journals of Captain Cook": "Cook's meticulous logs from three Pacific voyages, charting unknown waters and encountering indigenous peoples from Tahiti to Antarctica.",
    "A Turn in the South": "V.S. Naipaul's journey through the American South, exploring race, religion, and identity in the land of faulkner and civil rights struggles.",
    "The Zanzibar Chest": "A war correspondent's family memoir intertwined with African conflicts, uncovering his father's colonial past through a mysterious wooden chest of secrets.",
    "Imperium": "Kapuściński travels through the crumbling Soviet Union, witnessing the death of an empire and the human costs of totalitarianism's collapse.",

    # Category VIII: Political Moral and Historical Reckonings
    "A Dragon Apparent": "Norman Lewis travels through French Indochina in 1950, just before the wars, capturing Vietnam, Cambodia, and Laos on the eve of destruction.",
    "Travels with Herodotus": "Kapuściński carries Herodotus as his guide while reporting from revolutionary Iran, India, and China, finding ancient patterns in modern conflicts.",
    "A Lady's Life in the Rocky Mountains": "Victorian lady Isabella Bird rides solo through Colorado's Wild West in 1873, defying corsets and convention to climb mountains and befriend outlaws.",
    "Between the Woods and the Water": "Patrick Leigh Fermor's elegant sequel continuing his walk across 1930s Europe, from Hungary through Romania as storm clouds gather.",
    "The Geography of Bliss": "A grumpy journalist travels to the world's happiest and unhappiest countries, seeking the formula for national contentment from Iceland to Moldova.",
    "H is for Hawk": "Grieving her father's death, a woman trains a goshawk, intertwining her recovery with T.H. White's own falconry obsessions and escape from pain.",
    "The Japanese Journey": "Nicolas Bouvier's poetic wanderings through 1960s Japan, finding beauty in temples, tea ceremonies, and the tension between tradition and modernity.",

    # Category IX: Self-Reckoning Through Movement
    "The Colossus of Maroussi": "Henry Miller's ecstatic ode to Greece, celebrating light, friendship, and ancient landscapes that liberate the soul from modern despair.",
    "Stranger to History": "An Indian-Pakistani son searches for his estranged Muslim father, journeying through the Islamic world seeking identity, faith, and belonging.",
    "The Songlines": "Bruce Chatwin explores Aboriginal songlines—the invisible paths sung into existence that map Australia's landscape through myth and dreamtime.",
    "Wind, Sand and Stars": "Antoine de Saint-Exupéry's lyrical meditation on flight, the Sahara, and humanity, from the author who would later write The Little Prince.",
    "The Cloud Garden": "Two backpackers wander into Colombia's Darien Gap and spend nine months as guerrilla hostages, orchid-hunting and storytelling to stay sane.",
}

# Find book root and load config
book_root = find_book_root()
config = load_config(book_root)

# Build category mapping from config
category_to_dir = {}
for cat in config['categories']:
    cat_id = cat['id']
    cat_name = cat['name']
    roman_numerals = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX']
    cat_number = int(cat_id.split('_')[0]) if '_' in cat_id else 0
    if 0 < cat_number <= len(roman_numerals):
        full_name = f"{roman_numerals[cat_number - 1]}. {cat_name}"
        category_to_dir[full_name] = cat_id
    category_to_dir[cat_name] = cat_id

# Get paths
db_dir = get_book_path(book_root, 'database_dir')
writeups_dir = get_book_path(book_root, 'writeups_dir')

# Read honorable mentions
hm_path = db_dir / 'honorable-mentions.csv'
with open(hm_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    books = list(reader)

# Group by category
by_category = defaultdict(list)
for book in books:
    cat = book['Theme_Category']
    by_category[cat].append(book)

# Generate markdown files for each category
for category_name, category_dir in category_to_dir.items():
    books_in_cat = by_category.get(category_name, [])

    if not books_in_cat:
        continue

    # Sort by title
    books_in_cat.sort(key=lambda x: x['Title'])

    # Create markdown content
    content = f"# Honorable Mentions: {category_name}\n\n"
    content += f"_{len(books_in_cat)} additional books that belong in this category_\n\n"
    content += "---\n\n"

    for book in books_in_cat:
        title = book['Title']
        author = book['Author']
        region = book['Primary_Region']

        # Get the hand-crafted description
        description = descriptions.get(title, f"[Description needed for {title}]")

        # Format: **Title**, Author (Region) — Description
        content += f"**{title}**, {author} ({region}) — {description}\n\n"

    # Write to file
    file_path = writeups_dir / category_dir / 'honorable-mentions.md'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ Updated {file_path} ({len(books_in_cat)} books)")

print("\n" + "="*80)
print("✅ All honorable mentions updated with proper descriptions!")
print("="*80)
