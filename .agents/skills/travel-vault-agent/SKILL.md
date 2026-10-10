---
name: travel-vault-agent
description: Specialized agent for the Travel-Vault Obsidian workspace. Use when working with travel planning, itineraries, locations, logistics, or any content within the Travel-Vault. Triggers on tasks involving travel destinations (especially Japan), itinerary creation/editing, location management, budget planning, transport logistics, or vault organization. Also triggers when the user mentions Travel-Vault, Obsidian vault, travel knowledge base, or asks to add/edit/query travel-related content.
---

# Travel-Vault Agent

Skill specializzata per operare nel workspace Travel-Vault, valida per **qualsiasi harness** (opencode, Claude Code, Codex, Cursor…). Usa sempre **percorsi relativi alla root** del repository: il vault può essere aperto su Windows, macOS, Linux o in cloud.

> 📌 **Regole, fonti di verità, protocollo di modifica e privacy sono in `AGENTS.md`** (root). Questa skill aggiunge solo il "come" per struttura e contenuti: in caso di conflitto vale `AGENTS.md`.

## Tool

Negli esempi `read:` / `grep:` / `glob:` / `edit:` / `write:` / `bash:` indicano l'**azione** (leggi, cerca, trova, modifica, crea, esegui): usa lo strumento equivalente del tuo harness.

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
| `Città.md` | New city note | mapview + clusters + hotels |
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

1. `read: _templates/Città.md`
2. Scrivi in `Locations/<Country>/Cities/` con `write:`
3. Includi mapview block, cluster con `//`, ratings `#X/5`

## People & Interests

- **Lorenzo**: judo, anime, Akihabara, ramen
- **Davide, Rebecca**: nel gruppo del viaggio 2026
- **Group tags**: usare `#gruppoA`, `#gruppoB` per attività divise

## Current Trip

- **Destinazione**: Giappone (KIX → Izumisano → Osaka, Hiroshima, Nara, Kyoto, Tokyo)
- **Date**: 23 Ottobre (partenza) — 6 Novembre 2026 (rientro FCO 6 nov sera)
- **Persone**: Lorenzo, Davide, Rebecca
- **Stato prenotazioni**: leggere **sempre** `Info/Japan/Lista Prenotazioni.md` (fonte di verità — non copiarlo qui)
- **Budget e speso reale**: leggere `Info/Japan/Spese Reali.md` (fonte di verità)
- **Itinerari**: itinerario attivo in `Itinerari/Japan/2026/Itinerario-Giappone-23ott-6nov2026.md`

## Website Publishing

- Il sito Astro è in `_website/`
- `bash: cd _website && npm run build` (il sync è incluso nello script `build`)
- CI/CD automatico su push a `main` via GitHub Actions → **mai pushare su `main` senza conferma**
- Le note con `publish: false` e i blocchi `<!-- private -->…<!-- /private -->` non vengono pubblicati: vedi `AGENTS.md` → *Privacy e pubblicazione*
- Dopo ogni modifica: `bash: python3 _AI/scripts/vault_check.py`

## Obsidian CLI (opzionale)

Se Obsidian è in esecuzione con CLI attivato:
- `bash: obsidian search query="testo"` — Cerca nel vault
- `bash: obsidian read path="file.md"` — Legge file via Obsidian
- `bash: obsidian daily` — Apre la daily note
- `bash: obsidian daily:append content="- [ ] task"` — Aggiunge task
- `bash: obsidian create name="Nome" template=Location` — Crea nota da template
