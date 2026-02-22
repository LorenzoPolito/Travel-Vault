# Template Reference

Detailed reference for Obsidian templates in `_templates/`.

## Citta.md (City Note)

**Location**: `Locations/<Country>/Cities/<CityName>.md`

**Structure**:
- `mapview` code block with lat/lng coordinates and zoom level
- Embedded city photo `![[photo.jpg]]`
- `## Cibo tipico` section for local food
- `## Posti da visitare` with numbered lists separated by `//` clusters
  - Each item: `1. [[Location Name (kanji)]] (hours) #X/5`
  - Cluster = group of locations walkable in ~30min
- `## Hotels` with booking links

**YAML frontmatter fields**: `locations`, `tags`, `destination`

---

## Location.md (POI Note)

**Location**: `Locations/<Country>/<Category>/<LocationName>.md`

**Categories**: Temples, Parks-nature, Buildings, Stores, Castles, Hotels, Restaurants

**Structure**:
- Hero image `![Name](url)`
- Address in blockquote `> Address`
- Google Maps links (view + directions)
- `## Description` with intro text
- `### Da non perdere` bullet list
- `## Come arrivare` transport directions
- `### Storia e curiosita` historical notes
- `### Orari e tariffe` hours, cost, duration, closing day
- `### Consigli` tips

**YAML frontmatter fields**: `locations`, `tags`, `destination`, `city`, `rating`, `orari`, `costo`, `durata_visita`

---

## Itinerario.md (Basic Itinerary)

**Location**: `Itinerari/<Country>/<subfolder>/<ItineraryName>.md`

**Structure**:
- Author callout `> Creato da @Author`
- Budget table (city | days | nights | cost/night | notes)
- `## Alcune Info` section (timezone, passes, SIM)
- Day sections: `## Giorno N (description)`
  - Time blocks: `##### Mattina`, `##### Pomeriggio`, `##### Sera`
  - Activities as bullet lists with `[[wikilinks]]` to locations
  - Transport notes in italic `*Partenza verso X (Xmin)*`

**YAML frontmatter fields**: `tags`, `destination`, `durata_giorni`, `durata_notti`, `data_partenza`, `data_ritorno`, `status`, `autori`, `percorso`

---

## Itinerario Dettagliato.md (Detailed Itinerary)

**Location**: Same as basic itinerary

**Structure** (extends basic):
- Difficulty rating per day `**Difficolta fisica:** X/4`
- Minute-by-minute schedule table (Orario | Attivita | Note)
- `**Trasporti del giorno:**` section with exact routes
- `## Riepilogo Budget` summary table
- `## Prenotazioni da Fare` checklist with `- [ ]` items

**YAML frontmatter fields**: Same as basic + `budget_totale_stimato`

---

## Info.md (Information Note)

**Location**: `Info/<Country>/<Category>/<InfoName>.md`

**Structure**:
- `## Cos'e` description
- `## Dove si Compra` purchase options
- `## Copertura` coverage table
- `## Prezzi` pricing table
- `## Come si Usa` step-by-step guide
- `## Consigli` tips
- `## Link Utili` useful links

**YAML frontmatter fields**: `tags`, `destination`, `categoria`
