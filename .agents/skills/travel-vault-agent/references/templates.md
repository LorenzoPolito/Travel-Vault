# Template Reference

Detailed reference for Obsidian templates in `_templates/`.

## Città.md (City Note)

**Location**: `Locations/<Country>/Cities/<CityName>.md`

**Structure**:
- `mapview` code block with lat/lng coordinates and zoom level
- Embedded city photo `![[photo.jpg]]`
- `## Cibo tipico` — local food with descriptions
- `## Posti da visitare` — numbered lists separated by `//` clusters
  - Each item: `1. [[Location Name (kanji)]] (hours) #X/5`
  - Cluster = group of locations walkable in ~30min
  - Rating legend: `#5/5` = must-see → `#1/5` = skip
- `## Hotels` — booking links with zone
- `## Come muoversi` — airport transfer, metro lines, recommended passes

**YAML frontmatter fields**: `type: city`, `locations`, `destination`, `tags`

---

## Location.md (POI Note)

**Location**: `Locations/<Country>/<Category>/<LocationName>.md`

**Categories**: Temples, Parks-nature, Buildings, Stores, Castles, Hotels, Restaurants

**Structure**:
- Hero image `![Name](url)`
- Address in blockquote `> Address`
- Google Maps links (view + directions)
- `## Descrizione` — what it is, why visit
- `### Da non perdere` — bullet list of highlights
- `## Come arrivare` — specific lines, stations, walking times
- `## Storia e curiosità` — historical context
- `## Orari e tariffe` — structured table:
  | Orario | Giorno chiusura | Costo | Durata visita |
- `## Consigli` — practical tips (best time, what to bring)

**YAML frontmatter fields**: `type: location`, `category`, `destination`, `city`, `rating`, `orari`, `costo`, `durata_visita`, `tags`

---

## Itinerario.md (Basic Itinerary)

**Location**: `Itinerari/<Country>/<subfolder>/<ItineraryName>.md`

**Structure**:
- Author callout `> Creato da @Author`
- `## Sintesi` — budget table (city | days | nights | cost/night | notes)
- `## Info utili` — timezone, passes, IC card, eSIM
- Day sections: `## Giorno N — Description emoji`
  - Time blocks: `##### Mattina`, `##### Pomeriggio`, `##### Sera`
  - Activities as bullet lists with `[[wikilinks]]` to locations
  - Transport notes in italic `*Spostamento verso X (Xmin, linea Z)*`

**YAML frontmatter fields**: `type: itinerario`, `destination`, `durata_giorni`, `durata_notti`, `data_partenza`, `data_ritorno`, `status`, `autori`, `percorso`, `tags`

---

## Itinerario Dettagliato.md (Detailed Itinerary)

**Location**: Same as basic itinerary

**Key difference**: Every activity has a **specific time** (`**08:00**`, `**09:30**`, etc.)

**Structure** (extends basic):
- `## Considerazioni Generali` — budget, passes, travel style, fitness level
- `## Sintesi` — full budget table
- Day sections with **precise times**:
  - `**08:00** Activity description`
  - Each location entry includes:
    - *Livello di Difficoltà:* X/4
    - *Come Raggiungere:* specific line, station, time
    - *Consigli:* practical tip
  - Meals marked with 🍽️ emoji and budget
  - Transports in italic with lines and times
- `**Trasporti del giorno:**` — summary of all day's movements
- `## Riepilogo Budget` — detailed cost breakdown table
- `## Prenotazioni da Fare` — checklist with `- [ ]` items
- `## Note e Consigli` — general tips

**YAML frontmatter fields**: Same as basic + `budget_totale_stimato`

---

## Info.md (Information Note)

**Location**: `Info/<Country>/<Category>/<InfoName>.md`

**Structure**:
- `## Cos'è` — what it is and why it's useful
- `## Dove si Compra` — structured table (method | details)
- `## Copertura` — table (covers | doesn't cover)
- `## Prezzi` — table (type/duration | price | notes)
- `## Come si Usa` — numbered step-by-step guide
- `## Consigli` — practical tips
- `## Link Utili` — official sites, guides

**YAML frontmatter fields**: `type: info`, `destination`, `category`, `tags`
