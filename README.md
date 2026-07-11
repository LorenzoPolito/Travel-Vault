# Travel-Vault

**Vault Obsidian** per pianificazione viaggi + **sito Astro** pubblicato su GitHub Pages + **sistema AI** basato su opencode.

## Contenuto

- **Giappone 2026** — Viaggio attivo (24 Ott — 7 Nov, 14 notti)
- **Italia 2025** — Calabria (archiviato)

## Struttura

| Cartella | Contenuto |
|----------|-----------|
| `_AI/` | Knowledge base per agenti AI (indice, destinazioni, logistica) |
| `_templates/` | Template Obsidian per nuove note |
| `Info/Japan/` | Guide: IC Cards, JR Pass, eSIM, voli, sicurezza |
| `Itinerari/Japan/` | 19 varianti itinerario Giappone |
| `Locations/Japan/` | 76 location con rating, cluster, orari |
| `_website/` | Sito Astro con mappe Leaflet e ricerca Pagefind |
| `.agents/skills/` | Skill per agenti AI |

## Comandi Rapidi

| Comando | Descrizione |
|---------|-------------|
| `build:website` | Sync vault + build sito Astro |
| `sync:content` | Solo sync vault → Astro |
| `dev:website` | Sito in dev mode |

## Per Agenti AI

Leggi `AGENTS.md` per istruzioni. Config in `opencode.jsonc`.
