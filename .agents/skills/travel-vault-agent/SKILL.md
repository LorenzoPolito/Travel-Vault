---
name: travel-vault-agent
description: Specialized agent for the Travel-Vault Obsidian workspace. Use when working with travel planning, itineraries, locations, logistics, or any content within the Travel-Vault. Triggers on tasks involving travel destinations (especially Japan), itinerary creation/editing, location management, budget planning, transport logistics, or vault organization. Also triggers when the user mentions Travel-Vault, Obsidian vault, travel knowledge base, or asks to add/edit/query travel-related content.
---

# Travel-Vault Agent

Specialized skill for operating within the Travel-Vault Obsidian workspace located at `c:\Users\loren\Documents\TravelBay\Travel-Vault`.

## Vault Overview

This is a modular travel-planning Obsidian vault. Primary focus: **Japan trip (Feb-Mar 2026)** for Lorenzo + friends. Language: Italian.

## Entry Points

Always start from the AI knowledge hub:

1. **Master index**: `_AI/INDEX.md` - Full vault tree + quick reference table
2. **Conventions**: `_AI/README.md` - Vault rules and agent instructions
3. **Workspace metadata**: `_AI/knowledge/workspace.md` - Global vault info

## Key Conventions

| Convention | Meaning |
|---|---|
| `[[wikilink]]` | Obsidian internal link (not a URL) |
| `#X/5` | Location priority/interest rating (5=must-see, 1=skip) |
| `//` in location lists | Geographic cluster separator (walkable group) |
| `mapview` code block | Leaflet interactive map (Obsidian only) |
| `---` YAML frontmatter | File metadata block |
| `kanban-plugin: basic` | Kanban board file |

## Vault Structure

```
Travel-Vault/
  _AI/                   -> AI knowledge hub (read first)
  _templates/            -> Obsidian templates for new documents
  Info/                  -> Guides (IC Cards, JR Pass, eSIM, flights, safety)
  Itinerari/             -> All itinerary versions by destination
  Locations/             -> Location notes by category and destination
  Documenti Esterni/     -> External docs (PDF, DOCX)
  allegati/              -> Images and attachments
```

## Working with Destinations

Each destination has knowledge files in `_AI/knowledge/destinations/<name>/`:
- `locations.md` - All locations with ratings and clusters
- `itinerari.md` - Itinerary variants summary
- `logistica.md` - Transport, passes, budget, booking

### Adding a New Destination

1. Copy templates from `_AI/templates/` to `_AI/knowledge/destinations/<new>/`
2. Fill in the copied files with real data
3. Update `_AI/INDEX.md` (tree + quick reference table)

## Working with Templates

Obsidian templates live in `_templates/`. See `references/templates.md` for details on each template type.

### Template Types

| Template | Use Case |
|---|---|
| `Citta.md` | New city note (mapview + clusters + hotels) |
| `Location.md` | New location (temple, park, building, store) |
| `Itinerario.md` | Basic day-by-day itinerary |
| `Itinerario Dettagliato.md` | Detailed itinerary (minute-by-minute, difficulty, budget) |
| `Info.md` | Info note (pass, transport, SIM, safety) |

## Creating Content

### New Location Note

1. Use `_templates/Location.md` template
2. Place in `Locations/<Country>/<Category>/`
3. Categories: Temples, Parks-nature, Buildings, Stores, Castles, Hotels, Restaurants
4. Include: hero image, address, Google Maps link, "Da non perdere", "Come arrivare", hours/prices
5. Add to the city's location list with rating `#X/5` and cluster position

### New Itinerary

1. Use `_templates/Itinerario.md` or `_templates/Itinerario Dettagliato.md`
2. Place in `Itinerari/<Country>/<subfolder>/`
3. Use `[[wikilinks]]` for all location references
4. Include budget table, transport times, difficulty levels
5. Update `_AI/knowledge/destinations/<dest>/itinerari.md`

### New City Note

1. Use `_templates/Citta.md`
2. Place in `Locations/<Country>/Cities/`
3. Include mapview block, location clusters with `//` separators, ratings `#X/5`
4. Cluster locations by walkability (reachable in ~30min by foot/metro)

## People & Interests

- **Lorenzo**: judo, anime, Akihabara, ramen
- **Damiano**: Harry Potter (Warner Bros Studio Tour Tokyo)
- **Group tags**: `#gruppoA`, `#gruppoB` for split-day activities

## Current Trip Status

- **Destination**: Japan (Tokyo, Kyoto, Osaka, Hiroshima + day trips)
- **Dates**: Feb-Mar 2026, ~14 days
- **Status**: Planning phase, no definitive itinerary yet (18+ variants exist)
- **Budget**: ~1000-1100 EUR/person estimated (flights excluded)
