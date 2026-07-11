---
type: ai-index
scope: vault-root
vault: Travel-Vault
vault_path: "c:\\Users\\loren\\Documents\\TravelBay\\Travel-Vault"
language: it
last_updated: 2026-07-11
tags: [index, ai, vault-map, travel]
ai_role: "Master index del vault e della cartella _AI. Entry point principale per agenti."
---

# 🗂️ INDEX — Travel-Vault

---

## Vault Root

```
Travel-Vault/
│
├── Index.md                              ← Indice Obsidian (flat, wikilinks)
├── Itinerario Kanban Template.md         ← Template Kanban pasti
├── README.md                             ← Descrizione progetto
├── AGENTS.md                             ← ★ Istruzioni agente opencode (leggimi)
├── opencode.jsonc                        ← ★ Configurazione agente opencode
├── SKILL.md                              ← Skill root (stub)
│
├── _templates/                           ← ★ Template Obsidian per nuovi doc
│   ├── Città.md                          ← mapview + cluster + hotel
│   ├── Location.md                       ← hero + Google Maps + sezioni
│   ├── Itinerario.md                     ← tabella budget + giorno-per-giorno
│   ├── Itinerario Dettagliato.md         ← orari al minuto + difficoltà + budget
│   └── Info.md                           ← pass, trasporti, SIM, sicurezza
│
├── _AI/                                  ← ★ AI KNOWLEDGE HUB (questo file è qui)
│   ├── INDEX.md                          ← ★ Questo file — master index
│   ├── README.md                         ← Entry point e convenzioni vault
│   │
│   ├── knowledge/
│   │   ├── workspace.md                  ← Metadati vault-wide
│   │   └── destinations/
│   │       ├── japan/
│   │       │   ├── locations.md          ← 76 luoghi JP con voti e cluster
│   │       │   ├── itinerari.md          ← Itinerari JP (19 varianti)
│   │       │   └── logistica.md          ← IC Cards, JR Pass, budget JP
│   │       └── italia/
│   │           └── itinerari.md          ← Calabria 2025 (archiviato)
│   │
│   └── templates/                        ← Per aggiungere nuove destinazioni
│       ├── locations.md                  ← Template locations
│       ├── itinerari.md                  ← Template itinerari
│       ├── logistica.md                  ← Template logistica
│       └── How to Plan an Itinerary - Best Practices.md   ← ★ Metodologia completa
│
├── Info/
│   └── Japan/
│       ├── IC Cards/
│       ├── Pass/
│       ├── E-Sim/
│       ├── Voli/
│       └── Viaggiare Sicuri.md
│
├── Itinerari/
│   ├── Calabria/[ARCHIVIATO]
│   └── Japan/
│       ├── 2026/                         ★ Itinerario ATTIVO (24ott-7nov)
│       │   └── Itinerario-Osaka-Hiroshima-Kyoto-Tokyo-dettagliato-(14notti)-24ott-7nov.md
│       ├── Esterni/
│       └── Solo con i luoghi/
│           ├── 7 giorni/    (×2)
│           ├── 10 giorni/   (×2)
│           ├── 11 giorni/   (×2)
│           ├── 12 giorni/   (×1)
│           ├── 14 giorni/   (×9)
│           ├── 15 giorni/   (×1)
│           └── 16 giorni/   (×1)
│
├── Locations/
│   └── Japan/
│       ├── Lista dei Luoghi.md           ← ★ Master list: voti + cluster
│       ├── Cities/         (×9)
│       ├── Temples/        (×25)
│       ├── Parks-nature/   (×11)
│       ├── Buildings/      (×5)
│       ├── Stores/         (×5)
│       ├── Castles/        (×2)
│       ├── Hotels/         (×1)
│       └── Restaurants/    (×1)
│
├── Documenti Esterni/
├── allegati/
│
├── _website/                             ← ★ Sito Astro (GitHub Pages)
│   └── ...                               ← Build: npm run build:website
│
└── .agents/
    └── skills/
        ├── travel-vault-agent/SKILL.md   ← ★ Skill principale
        ├── git-flow-expert/SKILL.md      ← Git Flow workflow
        └── ...                           ← Altre skill installate
```

---

## 🤖 Quick Reference per Agenti AI

| Obiettivo | File da leggere |
| --- | --- |
| Overview vault e convenzioni | `_AI/knowledge/workspace.md` |
| Overview vault + convenzioni | `AGENTS.md` o `_AI/knowledge/workspace.md` |
| Luoghi JP con voti e orari | `_AI/knowledge/destinations/japan/locations.md` |
| Stato itinerari Giappone | `_AI/knowledge/destinations/japan/itinerari.md` |
| Trasporti, pass, budget JP | `_AI/knowledge/destinations/japan/logistica.md` |
| Skill principale agente | `.agents/skills/travel-vault-agent/SKILL.md` |
| Configurazione agente | `opencode.jsonc` |
| Viaggio Italia (archiviato) | `_AI/knowledge/destinations/italia/itinerari.md` |
| Aggiungere nuova destinazione | Copia da `_AI/templates/` |

---

## 📐 Come Scalare la Knowledge Base

Quando si aggiunge una nuova destinazione (es. Francia):

```
1. Crea cartella: _AI/knowledge/destinations/france/
2. Copia i template da _AI/templates/
3. Compila i file copiati con il contenuto reale
4. Aggiorna questo INDEX.md (aggiungi riga all'albero e alla table sopra)
5. Aggiorna _AI/README.md se necessario
```

---

## 📌 Convenzioni Vault

| Convenzione | Significato |
| --- | --- |
| `[[wikilink]]` | Link interno Obsidian (non è un URL) |
| `#X/5` | Priorità/interesse di un luogo (5=must, 1=skip) |
| `//` in liste | Separatore cluster geografico |
| `leaflet` code block | Mappa interattiva (solo in Obsidian) |
| `---` frontmatter YAML | Metadata del file |
| `kanban-plugin: basic` | File Kanban (solo in Obsidian) |
