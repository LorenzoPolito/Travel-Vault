---
name: travel-vault-agent
description: Specialized agent for the Travel-Vault Obsidian workspace. Use when working with travel planning, itineraries, locations, logistics, or any content within the Travel-Vault. Triggers on tasks involving travel destinations (especially Japan), itinerary creation/editing, location management, budget planning, transport logistics, or vault organization. Also triggers when the user mentions Travel-Vault, Obsidian vault, travel knowledge base, or asks to add/edit/query travel-related content.
---

# Travel-Vault Agent

Skill specializzata per operare nel workspace Travel-Vault. Il vault si trova su Windows.

## Tool Reference (Opencode)

Usa questi tool per operare nel vault:

- `read:` — Leggi file del vault
- `grep:` — Cerca contenuti nel vault
- `glob:` — Trova file per pattern
- `edit:` — Modifica file esistenti
- `write:` — Crea nuovi file
- `bash:` — Esegui comandi (git, npm, python, obsidian)

Se Obsidian CLI è attivo, usa `bash: obsidian search/read/daily/create` per interagire col vault via app.

## Vault Overview

Vault modulare per pianificazione viaggi. Focus primario: **Giappone, 23 Ott — 6 Nov 2026** per Lorenzo + Davide + Rebecca. Lingua: Italiano.

## Entry Points (leggi sempre prima questi)

1. **`read: _AI/INDEX.md`** — Full vault tree + quick reference table
2. **`read: _AI/README.md`** — Vault rules and agent instructions
3. **`read: _AI/knowledge/workspace.md`** — Global vault info

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
  Info/Japan/            -> Guides (IC Cards, JR Pass, eSIM, flights, safety)
  Itinerari/Japan/       -> All itinerary versions
  Locations/Japan/       -> Location notes by category
  _website/              -> Astro static site (published to GitHub Pages)
```

## Working with Destinations

Ogni destinazione ha file knowledge in `_AI/knowledge/destinations/<name>/`:
- `read: <dest>/locations.md` — All locations with ratings and clusters
- `read: <dest>/itinerari.md` — Itinerary variants summary
- `read: <dest>/logistica.md` — Transport, passes, budget, booking

### Aggiungere una Nuova Destinazione

1. `glob: _AI/templates/*` per vedere i template disponibili
2. Crea `_AI/knowledge/destinations/<nuova>/` con copie dei template
3. Compila i file con dati reali (`edit:` / `write:`)
4. Aggiorna `_AI/INDEX.md` (tree + quick reference table) con `edit:`

## Working with Templates

Obsidian templates in `_templates/`. Dettagli in `references/templates.md`.

### Template Types

| Template | Use Case | Struttura |
|---|---|---|
| `Citta.md` | New city note | mapview + clusters + hotels |
| `Location.md` | New POI | hero image + Google Maps + sections |
| `Itinerario.md` | Basic itinerary | budget table + day-by-day |
| `Itinerario Dettagliato.md` | Detailed itinerary | minute-by-minute + difficulty + budget |
| `Info.md` | Info/resource note | structured sections |

## Creating Content

### Nuova Location

1. `read: _templates/Location.md` — copia la struttura
2. Scrivi in `Locations/<Country>/<Category>/` con `write:`
3. Categorie: Temples, Parks-nature, Buildings, Stores, Castles, Hotels, Restaurants
4. Includi: hero image, address, Google Maps link, "Da non perdere", "Come arrivare", hours/prices
5. Aggiungi rating `#X/5` e cluster position nella città corrispondente

### Nuovo Itinerario

1. `read: _templates/Itinerario Dettagliato.md`
2. Scrivi in `Itinerari/Japan/Solo con i luoghi/<N giorni>/` con `write:`
3. Usa `[[wikilinks]]` per riferimenti a location
4. Includi budget table, transport times, difficulty levels
5. Aggiorna `_AI/knowledge/destinations/japan/itinerari.md`

### Nuova Città

1. `read: _templates/Citta.md`
2. Scrivi in `Locations/<Country>/Cities/` con `write:`
3. Includi mapview block, cluster con `//`, ratings `#X/5`

## People & Interests

- **Lorenzo**: judo, anime, Akihabara, ramen
- **Davide, Rebecca**: nel gruppo del viaggio 2026
- **Group tags**: usare `#gruppoA`, `#gruppoB` per attività divise

## Current Trip Status

- **Destinazione**: Giappone (KIX → Izumisano → Osaka, Hiroshima, Nara, Kyoto, Tokyo)
- **Date**: 23 Ottobre (partenza) — 6 Novembre 2026 (15gg/14notti)
- **Persone**: Lorenzo, Davide, Rebecca
- **Budget stimato**: ~2.936 €/persona (voli inclusi 1.096 €)
- **Stato**: ✅ **VOLI PRENOTATI** (China Eastern open-jaw, 09/08/26) · ✅ **Alloggi prenotati** · ❌ attività da prenotare (USJ, TeamLab, JR Kansai-Hiroshima Pass, Fuji Excursion, eSIM, assicurazione)
- **Voli**: FCO→KIX 23/10 21:10 (via Shanghai) · HND→FCO 6/11 08:40 (via Shanghai)
- **JR Pass**: NON consigliato — meglio JR Kansai-Hiroshima 5gg (~99€) + biglietto singolo Kyoto→Tokyo (~81€)
- **Itinerari**: itinerario attivo in `Itinerari/Japan/2026/Itinerario-Giappone-23ott-6nov2026.md`

## Website Publishing

- Il sito Astro è in `_website/`
- `bash: cd _website && node scripts/sync-content.mjs && npm run build` per buildare
- CI/CD automatico su push a `main` via GitHub Actions

## Obsidian CLI (opzionale)

Se Obsidian è in esecuzione con CLI attivato:
- `bash: obsidian search query="testo"` — Cerca nel vault
- `bash: obsidian read path="file.md"` — Legge file via Obsidian
- `bash: obsidian daily` — Apre la daily note
- `bash: obsidian daily:append content="- [ ] task"` — Aggiunge task
- `bash: obsidian create name="Nome" template=Location` — Crea nota da template
