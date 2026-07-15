# Travel-Vault — Istruzioni per l'Agente

## Overview

Questo workspace è un **Obsidian vault** per pianificazione viaggi + un **sito Astro** pubblicato su GitHub Pages + un **sistema di agenti AI**.

## Entry Points

1. **Config agente**: `opencode.jsonc` — configurazione agente, permessi, istruzioni
2. **AI Knowledge Hub**: `_AI/INDEX.md` — vault tree + quick reference table
3. **Workspace metadata**: `_AI/knowledge/workspace.md` — info globale vault
4. **Skill principale**: `.agents/skills/travel-vault-agent/SKILL.md`

## Viaggio Attivo

- **Giappone**: 24 Ott — 7 Nov 2026 (15gg/14notti)
- **Persone**: Lorenzo, Davide, Rebecca
- **Route**: Osaka → Hiroshima → Nara → Kyoto → Tokyo
- **Budget**: ~2.440-2.640 €/persona
- **Stato**: Pianificazione definita, prenotazioni da fare

## Convenzioni Vault

| Convenzione | Significato |
|---|---|
| `[[wikilink]]` | Link interno Obsidian |
| `#X/5` | Priorità luogo (5=must, 1=skip) |
| `//` in liste | Separatore cluster geografico |
| `leaflet`/`mapview` | Mappe interattive (solo Obsidian) |
| `---` frontmatter | Metadata YAML |

## Skill Disponibili

| Skill | Path | Quando usarla |
|---|---|---|
| Travel-Vault Agent | `.agents/skills/travel-vault-agent/SKILL.md` | Skill principale per operare nel vault |
| Obsidian CLI | `.agents/skills/obsidian-cli/SKILL.md` | Per interagire col vault via CLI Obsidian |
| Travel Web Research | `.agents/skills/travel-web-research/SKILL.md` | Ricerca web su ristoranti, trasporti, attrazioni |
| Git Flow Expert | `.agents/skills/git-flow-expert/SKILL.md` | Git Flow workflow per il progetto |

## Tool Disponibili

- **Obsidian CLI** (se attivo, richiede Obsidian in esecuzione): `obsidian search/read/daily/create/tasks`
- **Website**: `npm run build:website` per sync + build Astro

## Comandi Rapidi

- `build:website` — Sync vault content + build sito
- `sync:content` — Solo sync vault → Astro
- `dev:website` — Sito in development mode

## Monitoraggio Voli (check ogni 2 giorni)

Ogni 2 giorni (15, 17, 19, 21, 23, 25, 27, 29, 31 Lug + 1-3 Ago), l'agente DEVE:
1. Cercare **FCO→KIX 24 Ott** su Google Flights (cercare "Rome to Tokyo" come proxy — KIX non dà risultati)
2. Cercare **TYO→FCO 6 Nov** su Google Flights
3. Aggiornare `Calendario Monitoraggio` nell'itinerario
4. Se il prezzo totale A/R scende sotto **€1.000/pax**, segnalare come 🎯 **OFFERTA**
5. Target prenotazione: **inizio Agosto 2026**
