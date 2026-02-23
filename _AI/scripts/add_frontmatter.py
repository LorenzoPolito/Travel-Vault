#!/usr/bin/env python3
"""
Add YAML frontmatter to all markdown files in the Travel-Vault.
Only adds frontmatter to files that don't already have it.
Content is never modified — only a YAML block is prepended.
"""

import os
import re
from pathlib import Path

VAULT = Path(r"c:\Users\loren\Documents\TravelBay\Travel-Vault")

# Category -> tag mapping for Info files
INFO_CATEGORY_TAGS = {
    "IC Cards": ["trasporti", "ic-card"],
    "Pass": ["trasporti", "pass"],
    "E-Sim": ["comunicazione", "esim"],
    "Voli": ["trasporti", "voli"],
}

# Location category -> tag
LOCATION_CATEGORY_TAGS = {
    "Temples": "tempio",
    "Parks-nature": "parco",
    "Buildings": "edificio",
    "Stores": "negozio",
    "Castles": "castello",
    "Hotels": "hotel",
    "Restaurants": "ristorante",
    "Cities": "city",
}

# City associations for locations (derived from vault knowledge)
# Location name substring -> city
CITY_MAP = {
    # Tokyo locations
    "Senso-Ji": "Tokyo", "Asakusa": "Tokyo", "Akihabara": "Tokyo",
    "Tokyo skytree": "Tokyo", "Tokyo tower": "Tokyo", "Ueno": "Tokyo",
    "Shibuya": "Tokyo", "Shinjuku": "Tokyo", "Meiji": "Tokyo",
    "Kanda": "Tokyo", "Kodokan": "Tokyo", "Golden Gai": "Tokyo",
    "Nakano": "Tokyo", "harry potter": "Tokyo", "Rainbow Bridge": "Tokyo",
    "Tsukiji": "Tokyo", "Roppongi": "Tokyo", "Ginza": "Tokyo",
    "Odaiba": "Tokyo", "Palazzo Imperiale": "Tokyo", "Mario kart": "Tokyo",
    "Pokemon center Asakusa": "Tokyo", "Pokemon center Shibuya": "Tokyo",
    "Harajuku": "Tokyo",
    # Kyoto locations
    "Kiyomizu": "Kyoto", "Nishiki": "Kyoto", "Fushimi": "Kyoto",
    "Kinkaku": "Kyoto", "Ryoan": "Kyoto", "Arashiyama": "Kyoto",
    "Adashino": "Kyoto", "Gion": "Kyoto", "Yasaka": "Kyoto",
    "Kodai-ji": "Kyoto", "Daikaku": "Kyoto", "Ginkaku": "Kyoto",
    "Sannenzaka": "Kyoto", "TOEI": "Kyoto", "Sentiero del filosofo": "Kyoto",
    "Ninenzaka": "Kyoto", "Ninen": "Kyoto",
    # Osaka locations
    "Castello di Osaka": "Osaka", "Umeda": "Osaka", "Dotonbori": "Osaka",
    "Shitenno": "Osaka", "Shinsekai": "Osaka", "Tsutenkaku": "Osaka",
    "Hozen-ji": "Osaka", "Universal Studios": "Osaka", "Teamlab": "Osaka",
    "Kaiyukan": "Osaka",
    # Hiroshima locations
    "Memorial Park Hiroshima": "Hiroshima", "Nagarekawa": "Hiroshima",
    "Hondori": "Hiroshima",
    # Kamakura locations
    "Kutoku": "Kamakura", "Kencho": "Kamakura", "Engaku": "Kamakura",
    "Hokoku": "Kamakura", "Tsurugaoka": "Kamakura", "Hasedera": "Kamakura",
    # Miyajima locations
    "Itsukushima": "Miyajima", "Daisho-in": "Miyajima", "Monte Misen": "Miyajima",
    # Fujiyoshida
    "Chureito": "Fujiyoshida", "Kanandorii": "Fujiyoshida",
}

def has_frontmatter(content: str) -> bool:
    """Check if file already has YAML frontmatter."""
    return content.lstrip('\ufeff').startswith('---')

def detect_city(filename: str, parts: list) -> str:
    """Try to detect which city a location belongs to."""
    for key, city in CITY_MAP.items():
        if key.lower() in filename.lower():
            return city
    return ""

def get_destination(parts: list) -> str:
    """Extract destination from path parts."""
    for p in parts:
        if p == "Japan":
            return "Japan"
        if p == "Calabria":
            return "Italia"
    return ""

def get_duration_from_path(filepath: Path) -> str:
    """Extract duration from itinerary path."""
    for part in filepath.parts:
        match = re.match(r'(\d+)\s*giorni', part)
        if match:
            return f"{match.group(1)} giorni"
    return ""

def generate_frontmatter(filepath: Path, rel_parts: list) -> str:
    """Generate appropriate YAML frontmatter based on file path."""
    filename = filepath.stem
    
    # --- LOCATIONS ---
    if "Locations" in rel_parts:
        destination = get_destination(rel_parts)
        dest_tag = destination.lower() if destination else ""
        
        # Determine category
        category = ""
        category_tag = ""
        for cat, tag in LOCATION_CATEGORY_TAGS.items():
            if cat in rel_parts:
                category = cat
                category_tag = tag
                break
        
        # Cities
        if category == "Cities":
            # Blocks/quarters
            if "blocks" in rel_parts:
                if "streets" in rel_parts:
                    city = detect_city(filename, rel_parts)
                    tags = ["street", dest_tag] if dest_tag else ["street"]
                    return build_yaml(type="street", destination=destination, city=city, tags=tags)
                else:
                    city = detect_city(filename, rel_parts)
                    tags = ["quartiere", dest_tag] if dest_tag else ["quartiere"]
                    return build_yaml(type="quartiere", destination=destination, city=city, tags=tags)
            else:
                # Already has frontmatter (Tokyo, Kyoto, etc.) - skip handled by caller
                tags = ["city", "map", dest_tag] if dest_tag else ["city", "map"]
                return build_yaml(type="city", destination=destination, tags=tags)
        
        # Special: Lista dei Luoghi
        if "Lista dei Luoghi" in filename:
            tags = ["index", "locations", dest_tag] if dest_tag else ["index", "locations"]
            return build_yaml(type="index", destination=destination, tags=tags)
        
        # Hotels special
        if "Hotel-Hostel" in filename:
            tags = ["hotel", "alloggio", dest_tag] if dest_tag else ["hotel", "alloggio"]
            return build_yaml(type="info", destination=destination, category="alloggio", tags=tags)
        
        # Regular location
        city = detect_city(filename, rel_parts)
        tags = ["location", category_tag, dest_tag] if dest_tag else ["location", category_tag]
        tags = [t for t in tags if t]  # remove empty
        return build_yaml(type="location", destination=destination, category=category_tag, city=city, tags=tags)
    
    # --- ITINERARI ---
    if "Itinerari" in rel_parts:
        destination = get_destination(rel_parts)
        dest_tag = destination.lower() if destination else ""
        duration = get_duration_from_path(filepath)
        
        # External itinerary
        if "Esterni" in rel_parts:
            tags = ["itinerario", "esterno", dest_tag] if dest_tag else ["itinerario", "esterno"]
            return build_yaml(type="itinerario", destination=destination, durata=duration,
                            source="esterno", tags=tags)
        
        # Kanban
        if "Kanban" in filename:
            tags = ["kanban", "itinerario", dest_tag] if dest_tag else ["kanban", "itinerario"]
            return build_yaml(type="kanban", destination=destination, tags=tags)
        
        # Regular itinerary
        tags = ["itinerario", dest_tag] if dest_tag else ["itinerario"]
        tags = [t for t in tags if t]
        return build_yaml(type="itinerario", destination=destination, durata=duration, tags=tags)
    
    # --- INFO ---
    if "Info" in rel_parts:
        destination = get_destination(rel_parts)
        dest_tag = destination.lower() if destination else ""
        
        # Determine category
        category = ""
        category_tags = []
        for cat, ctags in INFO_CATEGORY_TAGS.items():
            if cat in rel_parts:
                category = cat.lower().replace(" ", "-")
                category_tags = ctags
                break
        
        # Safety file
        if "Viaggiare Sicuri" in filename:
            tags = ["info", "sicurezza", dest_tag] if dest_tag else ["info", "sicurezza"]
            return build_yaml(type="info", destination=destination, category="sicurezza", tags=tags)
        
        tags = ["info"] + category_tags + ([dest_tag] if dest_tag else [])
        tags = [t for t in tags if t]
        return build_yaml(type="info", destination=destination, category=category, tags=tags)
    
    return ""

def build_yaml(**kwargs) -> str:
    """Build a YAML frontmatter string from keyword arguments."""
    lines = ["---"]
    for key, value in kwargs.items():
        if value == "" or value is None:
            continue
        if key == "tags" and isinstance(value, list):
            value = [v for v in value if v]
            lines.append(f"tags:")
            for tag in value:
                lines.append(f"  - {tag}")
        else:
            lines.append(f"{key}: {value}")
    lines.append("---")
    return "\n".join(lines) + "\n"

def process_file(filepath: Path, vault_root: Path) -> bool:
    """Add frontmatter to a single file. Returns True if modified."""
    try:
        content = filepath.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        try:
            content = filepath.read_text(encoding='utf-8-sig')
        except:
            print(f"  SKIP (encoding): {filepath.name}")
            return False
    
    if has_frontmatter(content):
        return False
    
    rel = filepath.relative_to(vault_root)
    rel_parts = list(rel.parts)
    
    frontmatter = generate_frontmatter(filepath, rel_parts)
    if not frontmatter:
        print(f"  SKIP (no rule): {rel}")
        return False
    
    new_content = frontmatter + content
    filepath.write_text(new_content, encoding='utf-8')
    return True

def main():
    folders = [
        VAULT / "Locations",
        VAULT / "Itinerari",
        VAULT / "Info",
    ]
    
    total = 0
    modified = 0
    skipped_fm = 0
    
    for folder in folders:
        if not folder.exists():
            print(f"Folder not found: {folder}")
            continue
        
        md_files = sorted(folder.rglob("*.md"))
        print(f"\n{'='*60}")
        print(f"Processing: {folder.name}/ ({len(md_files)} files)")
        print(f"{'='*60}")
        
        for f in md_files:
            total += 1
            rel = f.relative_to(VAULT)
            
            try:
                content = f.read_text(encoding='utf-8')
            except:
                content = f.read_text(encoding='utf-8-sig')
            
            if has_frontmatter(content):
                skipped_fm += 1
                print(f"  EXISTS: {rel}")
                continue
            
            if process_file(f, VAULT):
                modified += 1
                print(f"  ADDED:  {rel}")
            else:
                print(f"  SKIP:   {rel}")
    
    print(f"\n{'='*60}")
    print(f"RESULTS:")
    print(f"  Total files:      {total}")
    print(f"  Already had FM:   {skipped_fm}")
    print(f"  Added FM:         {modified}")
    print(f"  Skipped:          {total - skipped_fm - modified}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
