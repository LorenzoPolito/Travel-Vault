---
type: ai-workspace-metadata
scope: global
vault: Travel-Vault
vault_path: "c:\\Users\\loren\\Documents\\TravelBay\\Travel-Vault"
language: it
last_updated: 2026-08-09
authors: [Lorenzo, Damiano]
tags: [metadata, vault, conventions, obsidian, travel]
ai_role: "Leggi questo file per capire la struttura e le convenzioni del vault prima di operare."
---

# Travel-Vault — Metadati Workspace

## Come Aggiornare

> Aggiorna questo file quando cambia la struttura del vault, vengono aggiunte destinazioni o cambiano le convenzioni. Aggiorna sempre `last_updated`.

---

## Descrizione

**Travel-Vault** è un vault Obsidian per la **pianificazione di viaggi in generale**.
Attualmente focalizzato su **Giappone** (contenuto principale) e con **Italia** (Calabria 2025, archiviato).

**Autori:** Lorenzo, Damiano · **Versioning:** Git (`.git/` in root)

---

## Struttura Cartelle

| Cartella | Contenuto | Note |
| --- | --- | --- |
| `_AI/` | Knowledge hub per agenti AI | Questa cartella |
| `Info/` | Info logistiche per destinazione | Attuale: solo Japan |
| `Itinerari/` | Itinerari per destinazione | Japan + Calabria |
| `Locations/` | Schede luoghi per destinazione | Attuale: solo Japan |
| `Documenti Esterni/` | PDF e DOCX da fonti esterne | — |
| `allegati/` | Immagini e allegati | — |

---

## Destinazioni Attive

| Destinazione | Stato | Cartelle principali |
| --- | --- | --- |
| 🇯🇵 Giappone | **Confermato — voli e alloggi prenotati** (23 ott — 6 nov 2026) | `Locations/Japan/`, `Itinerari/Japan/`, `Info/Japan/` |
| 🇺🇸 New York | **In pianificazione** (21-29 ago 2026) | `Itinerari/UnitedStates/NewYork/`, `Locations/UnitedStates/NewYork/`, `Info/NewYork/` |
| 🇮🇹 Italia | **Archiviato** (ago 2025) | `Itinerari/Calabria/` |

---

## Convenzioni Obsidian

| Elemento | Sintassi | Comportamento |
| --- | --- | --- |
| Wikilink | `[[Nome File]]` | Link interno — NON è un URL |
| Tag priorità | `#X/5` | 5=imperdibile, 1=skip |
| Cluster | `//` nelle liste | Separatore cluster geografico |
| Mappa | `leaflet` code block | Mappa interattiva (solo Obsidian) |
| Kanban | `kanban-plugin: basic` | Board Kanban (solo Obsidian) |
| Frontmatter | `---` YAML `---` | Metadata file |
| Callout | `> [!NOTE]` ecc. | Blocco evidenziato |

---

## Plugin Obsidian Usati

| Plugin | Uso nel vault |
| --- | --- |
| Leaflet | Mappe interattive nelle city notes |
| Kanban | Template pasti giornaliero |
| Dataview (possibile) | Query sui metadati (non verificato) |

---

## Struttura Modulare _AI

La cartella `_AI/` segue un'architettura **per-destinazione** scalabile:

```
_AI/knowledge/destinations/
├── japan/        ← Giappone (locations, itinerari, logistica)
├── italia/       ← Italia (itinerari)
└── [nuova]/      ← Copia da _AI/templates/ per aggiungere
```

**Per aggiungere una destinazione:**
1. Crea `_AI/knowledge/destinations/[paese]/`
2. Copia i file da `_AI/templates/`
3. Compila con il contenuto reale
4. Aggiorna `_AI/INDEX.md`

---

## Plugin e Feature Tecniche

- **Git:** versioning attivo, `.gitignore` presente
- **`Path.json`:** `{}` — placeholder non ancora usato
- **MagicTravel link:** hotel linkati in Kyoto e Osaka via `https://www.magictravel.ai/`
- **TBLFM:** formule tabelle inline in alcuni itinerari (es. somme budget)
