---
type: ai-readme
scope: ai-folder
vault: Travel-Vault
language: it
last_updated: 2026-02-23
tags: [ai, readme, conventions, entry-point]
ai_role: "Entry point per agenti AI. Leggere prima di qualsiasi altro file _AI."
---

# 🤖 _AI — Knowledge Hub per Agenti

Questa cartella contiene la **knowledge base strutturata** del vault **Travel-Vault**, pensata per essere letta e utilizzata da agenti AI. È modulare, scalabile e aggiornabile indipendentemente dal contenuto del vault.

---

## 📁 Struttura

```
_AI/
├── INDEX.md                    ← ★ Albero completo vault + quick reference
├── README.md                   ← Questo file
│
├── knowledge/
│   ├── workspace.md            ← Metadati globali, convenzioni, plugin
│   └── destinations/           ← Modulare per destinazione
│       ├── japan/
│       │   ├── locations.md    ← 76 luoghi con voti, orari, cluster
│       │   ├── itinerari.md    ← 18+ varianti, tempi percorrenza
│       │   └── logistica.md    ← IC Cards, JR Pass, budget, prenotazioni
│       └── italia/
│           └── itinerari.md    ← Calabria 2025 (archiviato)
│
└── templates/                  ← Copia per aggiungere nuove destinazioni
    ├── locations.md
    ├── itinerari.md
    └── logistica.md
```

---

## 🚀 Come Iniziare (per un agente)

1. **Leggi `INDEX.md`** — albero del vault + quick reference
2. **Leggi `knowledge/workspace.md`** — convenzioni e struttura
3. **Vai alla destinazione** in `knowledge/destinations/[paese]/`

---

## ➕ Aggiungere una Nuova Destinazione

```
1. mkdir _AI/knowledge/destinations/[paese]/
2. Copia i file da _AI/templates/
3. Compila i template con il contenuto reale del vault
4. Aggiorna _AI/INDEX.md (aggiungi all'albero e alla table)
5. Aggiorna last_updated nei frontmatter
```

---

## ⚠️ Convenzioni del Vault

| Sintassi | Significato |
| --- | --- |
| `[[wikilink]]` | Link interno Obsidian — non è un URL |
| `#X/5` | Voto priorità luogo (5=must, 1=bassa) |
| `//` nelle liste | Cambio cluster geografico |
| `leaflet` block | Mappa interattiva (solo Obsidian) |
