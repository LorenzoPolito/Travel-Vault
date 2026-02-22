---
type: ai-index
scope: vault-root
vault: Travel-Vault
vault_path: c:\Users\loren\Documents\TravelBay\Travel-Vault
language: it
last_updated: 2026-02-23
tags: [index, ai, travel, vault-map]
ai_role: "Entry point per agenti AI. Leggere prima di qualsiasi altro file _AI."
---

# 🗂️ INDEX — Travel-Vault

Indice ad albero completo del vault **Travel-Vault** e della cartella `_AI/`.

---

## Albero Completo del Vault

```
Travel-Vault/
│
├── Index.md                          ← Indice Obsidian (wikilinks flat)
├── Itinerario Kanban Template.md     ← Template Kanban pasti (kanban-plugin)
├── Path.json                         ← {} (placeholder)
│
├── _AI/                              ← [AI KNOWLEDGE HUB]
│   ├── INDEX.md                      ← ★ Questo file
│   ├── README.md                     ← Entry point e convenzioni vault
│   └── knowledge/
│       ├── workspace.md              ← Metadati, struttura, note tecniche
│       ├── locations.md              ← 76 luoghi con voti, orari, cluster
│       ├── itinerari.md              ← Stato e storia degli itinerari
│       └── logistica.md              ← IC Cards, JR Pass, budget, trasporti
│
├── Info/
│   └── Japan/
│       ├── IC Cards/
│       │   ├── IC Cards.md           ← Guida generale (~28KB)
│       │   ├── Suica.md              ← JR East, digitale su iPhone
│       │   ├── Pasmo.md              ← Operatori privati
│       │   └── Icoca.md              ← JR West / Kansai
│       ├── Pass/
│       │   ├── JR pass.md            ← Analisi completa (~15KB)
│       │   └── Osaka Amazing pass.md
│       ├── E-Sim/                    ← Opzioni eSIM per Giappone
│       ├── Voli/                     ← Info voli
│       └── Viaggiare Sicuri.md       ← Guida sicurezza (~31KB, max file)
│
├── Itinerari/
│   ├── Calabria/
│   │   └── Parghelia 2025.md         ← 9gg ago 2025 [ARCHIVIATO]
│   └── Japan/
│       ├── Esterni/
│       │   ├── Itinerario Ossama Valentina.md   ← Tokyo→Kyoto→Kobe→Hiroshima
│       │   └── Rail Adventure SiVola.it (14 gg).md
│       └── Solo con i luoghi/
│           ├── 7 giorni/    (×2)
│           ├── 10 giorni/   (×2)
│           ├── 11 giorni/   (×2)    ← Incl. versione dic 2025 (posticipata)
│           ├── 12 giorni/   (×1)
│           ├── 14 giorni/   (×8)    ← Principale — feb/mar 2026
│           ├── 15 giorni/   (×1)
│           └── 16 giorni/   (×1)
│
├── Locations/
│   └── Japan/
│       ├── Lista dei Luoghi.md       ← ★ Master list: voti + cluster
│       ├── Cities/         (×9)      ← Leaflet maps + lista luoghi
│       │   ├── Tokyo(東京).md
│       │   ├── Kyoto(京都).md
│       │   ├── Osaka(大阪市).md
│       │   ├── Hiroshima(広島).md
│       │   ├── Kamakura(鎌倉市).md
│       │   ├── Miyajima (宮島).md
│       │   ├── Nara (奈良市).md
│       │   ├── Fujiyoshida (富士吉田市).md
│       │   └── Kobe(神戸).md
│       ├── Temples/        (×25)     ← Templi e santuari
│       ├── Parks-nature/   (×11)     ← Parchi, attrazioni natura
│       ├── Buildings/      (×5)      ← Edifici iconici
│       ├── Stores/         (×5)      ← Mercati e negozi
│       ├── Castles/        (×2)
│       ├── Hotels/         (×1)
│       └── Restaurants/    (×1)
│
├── Documenti Esterni/
│   ├── Input Gamma.docx
│   ├── Itinerario Tokyo-Kyoto (11gg) (dic 2025).docx
│   ├── Itinerario Tokyo-Kyoto (11gg) (dic 2025).pdf
│   └── Viaggio in Giappone 2026.pdf
│
└── allegati/                         ← Immagini e allegati vari
```

---

## 🤖 Quick Reference per Agenti AI

| Hai bisogno di... | Leggi |
|---|---|
| Capire la struttura del vault | `_AI/knowledge/workspace.md` |
| Trovare un luogo con voti e orari | `_AI/knowledge/locations.md` |
| Sapere lo stato degli itinerari | `_AI/knowledge/itinerari.md` |
| Info su trasporti, budget, pass | `_AI/knowledge/logistica.md` |
| Tutti i luoghi (raw Obsidian) | `Locations/Japan/Lista dei Luoghi.md` |
| L'itinerario più recente | `Itinerari/Japan/Solo con i luoghi/14 giorni/Itinerario Tokyo-Kyoto-Osaka-Hiroshima-Tokyo(14 giorni)(15feb-1mar).md` |

---

## 📌 Note Architetturali

- **Nessun itinerario è "definitivo"** — tutti sono varianti di lavoro in evoluzione
- Il vault è per **viaggi in generale** (ora principalmente Giappone, + Calabria 2025)
- I **wikilink** `[[Nome]]` sono link interni Obsidian (non seguire come URL)
- Il separatore `//` nelle liste location = cambio cluster geografico
- Tag `#X/5` nelle location = punteggio priorità (5=must-see, 1=opzionale)
