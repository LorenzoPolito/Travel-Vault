---
type: ai-index
scope: vault-root
vault: Travel-Vault
vault_path: "c:\\Users\\loren\\Documents\\TravelBay\\Travel-Vault"
language: it
last_updated: 2026-02-23
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
├── Path.json                             ← {} placeholder
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
│   │       │   ├── itinerari.md          ← Itinerari JP (18 varianti)
│   │       │   └── logistica.md          ← IC Cards, JR Pass, budget JP
│   │       └── italia/
│   │           └── itinerari.md          ← Calabria 2025 (archiviato)
│   │
│   └── templates/                        ← Per aggiungere nuove destinazioni
│       ├── locations.md                  ← Template locations
│       ├── itinerari.md                  ← Template itinerari
│       └── logistica.md                  ← Template logistica
│
├── Info/
│   └── Japan/
│       ├── IC Cards/
│       │   ├── IC Cards.md               ← Guida generale (~28KB)
│       │   ├── Suica.md                  ← JR East / digitale iPhone
│       │   ├── Pasmo.md                  ← Operatori privati
│       │   └── Icoca.md                  ← JR West / Kansai
│       ├── Pass/
│       │   ├── JR pass.md                ← Analisi completa (~15KB)
│       │   └── Osaka Amazing pass.md
│       ├── E-Sim/
│       ├── Voli/
│       └── Viaggiare Sicuri.md           ← Guida sicurezza (~31KB)
│
├── Itinerari/
│   ├── Calabria/
│   │   └── Parghelia 2025.md             ← 9gg ago 2025 [ARCHIVIATO]
│   └── Japan/
│       ├── Esterni/
│       │   ├── Itinerario Ossama Valentina.md
│       │   └── Rail Adventure SiVola.it (14 gg).md
│       └── Solo con i luoghi/
│           ├── 7 giorni/    (×2)
│           ├── 10 giorni/   (×2)
│           ├── 11 giorni/   (×2)         ← Incl. versione dic 2025
│           ├── 12 giorni/   (×1)
│           ├── 14 giorni/   (×8)         ← ★ Principale — feb/mar 2026
│           ├── 15 giorni/   (×1)
│           └── 16 giorni/   (×1)
│
├── Locations/
│   └── Japan/
│       ├── Lista dei Luoghi.md           ← ★ Master list: voti + cluster
│       ├── Cities/         (×9)          ← Leaflet maps + lista luoghi
│       │   ├── Tokyo(東京).md
│       │   ├── Kyoto(京都).md
│       │   ├── Osaka(大阪市).md
│       │   ├── Hiroshima(広島).md
│       │   ├── Kamakura(鎌倉市).md
│       │   ├── Miyajima (宮島).md
│       │   ├── Nara (奈良市).md
│       │   ├── Fujiyoshida (富士吉田市).md
│       │   └── Kobe(神戸).md
│       ├── Temples/        (×25)
│       ├── Parks-nature/   (×11)
│       ├── Buildings/      (×5)
│       ├── Stores/         (×5)
│       ├── Castles/        (×2)
│       ├── Hotels/         (×1)
│       └── Restaurants/    (×1)
│
├── Documenti Esterni/
│   ├── Input Gamma.docx
│   ├── Itinerario Tokyo-Kyoto (11gg) dic 2025.docx + .pdf
│   └── Viaggio in Giappone 2026.pdf
│
└── allegati/                             ← Immagini e allegati vari
```

---

## 🤖 Quick Reference per Agenti AI

| Obiettivo | File da leggere |
| --- | --- |
| Overview vault e convenzioni | `_AI/knowledge/workspace.md` |
| Luoghi JP con voti e orari | `_AI/knowledge/destinations/japan/locations.md` |
| Stato itinerari Giappone | `_AI/knowledge/destinations/japan/itinerari.md` |
| Trasporti, pass, budget JP | `_AI/knowledge/destinations/japan/logistica.md` |
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
