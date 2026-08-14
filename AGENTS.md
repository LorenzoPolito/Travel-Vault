# Travel-Vault — Istruzioni per l'Agente

## Overview

Questo workspace è un **Obsidian vault** per pianificazione viaggi + un **sito Astro** pubblicato su GitHub Pages + un **sistema di agenti AI**.

## Entry Points

1. **Config agente**: `opencode.jsonc` — configurazione agente, permessi, istruzioni
2. **AI Knowledge Hub**: `_AI/INDEX.md` — vault tree + quick reference table
3. **Workspace metadata**: `_AI/knowledge/workspace.md` — info globale vault
4. **Skill principale**: `.agents/skills/travel-vault-agent/SKILL.md`

## Viaggio Attivo

- **Giappone**: 23 Ott (partenza) — 6 Nov 2026 (15gg/14notti)
- **Persone**: Lorenzo, Davide, Rebecca
- **Route**: Roma → KIX → Izumisano → Osaka → Hiroshima → Nara → Kyoto → Tokyo
- **Budget**: ~2.902 €/persona (voli inclusi 1.096 €)
- **Stato**: ✅ Voli prenotati (China Eastern, 1.096 €/pax) · ✅ Alloggi prenotati · ❌ attività da prenotare (USJ, TeamLab, PokéPark KANTO, JR Kansai-Hiroshima Pass, eSIM, assicurazione)

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

## Monitoraggio Voli ✅ COMPLETATO

I voli sono stati **prenotati il 09/08/26** (China Eastern open-jaw, 1.096,33 €/pax). Il monitoraggio periodico non è più necessario.

**Prenotazione:**
- 🛫 FCO→KIX 23/10 21:10 (MU788 + FM3051, via Shanghai PVG) → arrivo 24/10 21:00
- 🛬 HND→FCO 6/11 08:40 (MU576 + MU787, via Shanghai PVG) → arrivo 18:15
- Prezzo: 575,54 € andata + 520,79 € ritorno = 1.096,33 €/pax · tot. 3.289 € (3 pax)

**Attività ancora da prenotare:** USJ, TeamLab Planets, PokéPark KANTO, JR Kansai-Hiroshima Pass, eSIM, assicurazione.
