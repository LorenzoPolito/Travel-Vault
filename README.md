# Travel-Vault

**Vault Obsidian** per pianificazione viaggi + **sito Astro** pubblicato su GitHub Pages + **workspace agentico** (istruzioni comuni a tutti gli harness AI).

## Contenuto

- **Giappone 2026** — viaggio attivo: 23 Ott (partenza) — 6 Nov 2026 (rientro FCO 6 Nov sera)
- **New York 2026** — completato (21-29 Ago 2026)
- **Italia 2025** — Calabria (archiviato)

## Struttura

| Cartella | Contenuto |
|----------|-----------|
| `_AI/` | Knowledge base per agenti AI (indice, destinazioni, script di verifica) |
| `_templates/` | Template Obsidian per nuove note |
| `Info/` | Guide pratiche per destinazione (pass, trasporti, eSIM, prenotazioni, spese) |
| `Itinerari/` | Itinerario attivo + varianti storiche |
| `Locations/` | Schede luoghi con rating `#X/5`, cluster, orari |
| `_website/` | Sito Astro con mappe Leaflet e ricerca Pagefind |
| `.agents/skills/` | Skill per agenti AI |

## Comandi

Il sito vive in `_website/` (non c'è un `package.json` in root):

```bash
cd _website
npm ci              # prima volta
npm run sync        # solo sync vault → Astro
npm run dev         # sync + sito in dev mode
npm run build       # sync + build + indice ricerca
```

Verifica governance del vault (link, frontmatter, privacy):

```bash
python3 _AI/scripts/vault_check.py
```

## Privacy

La repository è **pubblica** e il sito è pubblico. Le note con `publish: false` nel frontmatter e i blocchi `<!-- private -->…<!-- /private -->` **non vengono pubblicati sul sito**, ma restano visibili nella repository GitHub. Dettagli in `AGENTS.md` → *Privacy e pubblicazione*.

## Per Agenti AI

Leggi **`AGENTS.md`**: è l'unica fonte di istruzioni per tutti gli harness (opencode, Claude Code, Codex, Cursor, …).
