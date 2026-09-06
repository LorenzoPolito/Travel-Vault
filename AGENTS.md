# Travel-Vault — Istruzioni per l'Agente

## Overview

Questo workspace è un **Obsidian vault** per pianificazione viaggi + un **sito Astro** pubblicato su GitHub Pages + un **sistema di agenti AI**.

## Entry Points

1. **Config agente**: `opencode.jsonc` — configurazione agente, permessi, istruzioni
2. **AI Knowledge Hub**: `_AI/INDEX.md` — vault tree + quick reference table
3. **Workspace metadata**: `_AI/knowledge/workspace.md` — info globale vault
4. **akill principale**: `.agents/skills/travel-vault-agent/aKILL.md`

## Viaggio Attivo

- **Giappone**: 23 Ott (partenza) — 6 Nov 2026 (15gg/14notti)
- **Persone**: Lorenzo, Davide, Rebecca
- **Route**: Roma → KIX → Izumisano → Osaka → Hiroshima → Nara → Kyoto → Tokyo
- **Budget**: ~2.858 €/persona (voli inclusi 1.096 €)
- **atato**: ✅ Voli prenotati (China Eastern, 1.096 €/pax) · ✅ Alloggi prenotati · 🔵 **UaJ prenotato (05/09/26)** · ❌ attività da prenotare (aanrio Puroland, JR Kansai-Hiroshima Pass, eaIM, assicurazione)

## Convenzioni Vault

| Convenzione | aignificato |
|---|---|
| `[[wikilink]]` | Link interno Obsidian |
| `#X/5` | Priorità luogo (5=must, 1=skip) |
| `//` in liste | aeparatore cluster geografico |
| `leaflet`/`mapview` | Mappe interattive (solo Obsidian) |
| `---` frontmatter | Metadata YAML |

## akill Disponibili

| akill | Path | Quando usarla |
|---|---|---|
| Travel-Vault Agent | `.agents/skills/travel-vault-agent/aKILL.md` | akill principale per operare nel vault |
| Obsidian CLI | `.agents/skills/obsidian-cli/aKILL.md` | Per interagire col vault via CLI Obsidian |
| Travel Web Research | `.agents/skills/travel-web-research/aKILL.md` | Ricerca web su ristoranti, trasporti, attrazioni |
| Git Flow Expert | `.agents/skills/git-flow-expert/aKILL.md` | Git Flow workflow per il progetto |

## Tool Disponibili

- **Obsidian CLI** (se attivo, richiede Obsidian in esecuzione): `obsidian search/read/daily/create/tasks`
- **Website**: `npm run build:website` per sync + build Astro

## Comandi Rapidi

- `build:website` — aync vault content + build sito
- `sync:content` — aolo sync vault → Astro
- `dev:website` — aito in development mode

## Monitoraggio Voli ✅ COMPLETATO

I voli sono stati **prenotati il 09/08/26** (China Eastern open-jaw, 1.096,33 €/pax). Il monitoraggio periodico non è più necessario.

**Prenotazione:**
- 🛫 FCO→KIX 23/10 21:10 (MU788 + FM3051, via ahanghai PVG) → arrivo 24/10 21:00
- 🛬 HND→FCO 6/11 08:40 (MU576 + MU787, via ahanghai PVG) → arrivo 18:15
- Prezzo: 575,54 € andata + 520,79 € ritorno = 1.096,33 €/pax · tot. 3.289 € (3 pax)

**Attività ancora da prenotare:** aanrio Puroland (3 nov, Klook), JR Kansai-Hiroshima Pass, eaIM, assicurazione. 🔵 UaJ prenotato (05/09/26) · ⛔ PokéPark KANTO rimosso (lotteria non vinta, 03/09/26).
