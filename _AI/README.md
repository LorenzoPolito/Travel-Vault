# 🤖 _AI — Cartella Agenti AI

Questa cartella contiene tutta la **knowledge base, i metadati e gli strumenti** necessari agli agenti AI per lavorare con il vault **Travel-Vault**.

Il contenuto di questa cartella è pensato per essere **condivisibile tra più agenti AI** (Antigravity, n8n, LangGraph, ecc.) e aggiornato progressivamente.

---

## 📁 Struttura

```
_AI/
├── README.md              ← Questo file (entry point per gli agenti)
├── knowledge/
│   ├── workspace.md       ← Metadati e struttura completa del vault
│   ├── locations.md       ← Knowledge base di tutti i luoghi
│   ├── itinerari.md       ← Stato e storia di tutti gli itinerari
│   └── logistica.md       ← IC Cards, JR Pass, eSIM, voli, sicurezza
└── tools/
    └── (placeholder per script/tool futuri)
```

---

## 🎯 Come usare questa cartella

1. **Inizia sempre da `knowledge/workspace.md`** — contiene una overview completa del vault, le convenzioni e i metadati.
2. **Per query sui luoghi**, usa `knowledge/locations.md`.
3. **Per query sugli itinerari**, usa `knowledge/itinerari.md`.
4. **Per info logistiche** (trasporti, pass, eSIM), usa `knowledge/logistica.md`.

---

## ⚠️ Convenzioni del Vault

- I **wikilink** `[[Nome Luogo]]` collegano le note internamente in Obsidian.
- I **tag** `#X/5` indicano la priorità/interesse di un luogo (da 1 a 5).
- Il separatore `//` nelle liste indica il cambio di **cluster geografico**.
- Le mappe sono renderizzate tramite il **plugin Leaflet** di Obsidian.
- Il vault usa **Git** per il versioning (`.git` nella root).
