# Travel-Vault — Istruzioni per gli Agenti

> **Unica fonte di istruzioni per tutti gli harness** (opencode, Claude Code, Codex, Cursor, Copilot, Gemini…).
> Gli altri file di configurazione (`CLAUDE.md`, `opencode.jsonc`, `.agent/workflows/`) **rimandano qui** e non aggiungono regole proprie.

## Cos'è

Questo workspace è un **vault Obsidian** per pianificare viaggi, più un **sito Astro** (`_website/`) pubblicato su GitHub Pages, più una **knowledge base per agenti** (`_AI/`). Lingua: **italiano**.

- Viaggio attivo: **Giappone, 23 Ott — 6 Nov 2026** · Lorenzo, Davide, Rebecca
- Itinerario: `Itinerari/Japan/2026/Itinerario-Giappone-23ott-6nov2026.md`

## 🧭 Fonti di verità

Ogni informazione ha **un solo file proprietario**. Gli altri file riportano al massimo un riassunto e **rimandano** al proprietario. Quando un dato cambia si aggiorna **prima il file proprietario**, poi i riassunti.

| Informazione | File proprietario |
|---|---|
| Stato prenotazioni (cosa è fatto / da fare / scadenze) | `Info/Japan/Lista Prenotazioni.md` |
| Soldi: budget, speso reale, saldi tra noi | `Info/Japan/Spese Reali.md` |
| Programma giorno per giorno, orari, budget giornaliero | `Itinerari/Japan/2026/Itinerario-Giappone-23ott-6nov2026.md` |
| Storico modifiche all'itinerario | `Itinerari/Japan/2026/Changelog Itinerario.md` |
| Finestre di prenotazione e prezzi delle attività | `Info/Japan/Attività e Prenotazioni.md` |
| Allergie Rebecca (sicurezza alimentare) | `Info/Japan/Allergie Alimentari Rebecca.md` |
| Sintesi per agenti (luoghi, itinerari, logistica) | `_AI/knowledge/destinations/<dest>/` |
| Mappa del vault | `_AI/INDEX.md` |

⛔ **Non usare come fonte** `_AI/archive/` (contenuti superati) né le varianti in `Itinerari/Japan/Solo con i luoghi/` (storiche).

> Lo stato delle prenotazioni **non va scritto** in questo file né nelle skill: leggerlo da `Info/Japan/Lista Prenotazioni.md`. Il controllo `vault_check.py` lo verifica.

## Protocollo di lavoro (obbligatorio)

Ogni modifica segue quattro passi. Non saltare al passo 3.

1. **Analizza** — leggi le fonti di verità coinvolte e cerca (`grep`) tutti i file che citano il dato.
2. **Valuta l'impatto** — elenca i file da toccare e cosa cambia. Se la modifica è ambigua, distruttiva (cancellazioni, cambi di struttura, cambi su cosa si pubblica) o tocca soldi/prenotazioni senza conferma dell'utente, **chiedi prima**.
3. **Agisci** — aggiorna il file proprietario, poi i riassunti (vedi tabella sotto), su un branch `feature/*`.
4. **Verifica** — esegui i controlli e riporta il risultato all'utente.

```bash
python3 _AI/scripts/vault_check.py          # sempre
cd _website && npm run build                # se hai toccato contenuti pubblicati o il sito
```

### Cosa aggiornare quando cambia…

| Cambia… | Aggiorna (in quest'ordine) |
|---|---|
| Una prenotazione (fatta, annullata, nuova scadenza) | `Lista Prenotazioni` → `Spese Reali` (se c'è un costo) → riga di stato dell'itinerario → `Changelog Itinerario` → `_AI/knowledge/destinations/japan/logistica.md` |
| Un costo o il budget | `Spese Reali` → totale nell'itinerario (frontmatter `budget_totale_stimato` + sezione budget) → KB logistica |
| Il programma di un giorno | Itinerario → `Changelog Itinerario` → KB itinerari (se cambia la sintesi) |
| Struttura cartelle, template, convenzioni | `_AI/INDEX.md` → `_AI/knowledge/workspace.md` → skill `travel-vault-agent` (+ `references/templates.md`) |
| Una nuova destinazione | `_AI/knowledge/destinations/<dest>/` (da `_AI/templates/`) → `_AI/INDEX.md` |

In ogni file toccato aggiorna `last_updated: YYYY-MM-DD` nel frontmatter.

## Output attesi

Ogni risposta che modifica il vault deve dire all'utente:
- **cosa** è cambiato e in **quali file** (percorsi relativi);
- l'esito di `vault_check.py` (e della build, se eseguita);
- cosa **resta da decidere o da fare** (con eventuali scadenze).

Date in formato `GG/MM/AA` nel testo e `YYYY-MM-DD` nel frontmatter. Importi in € con virgola decimale (`95,86 €`), yen come `¥13.650`. Orari giapponesi in **JST** (Italia −7h fino al 25 ott, −8h dopo).

## 🔒 Privacy e pubblicazione

La **repository GitHub è pubblica** e il sito è pubblico.

- Il sito pubblica `Locations/`, `Itinerari/`, `Info/`, **tranne**:
  - le note con `publish: false` nel frontmatter (non vengono pubblicate; i link verso di esse diventano testo);
  - il contenuto tra `<!-- private -->` e `<!-- /private -->` (visibile in Obsidian, rimosso dal sito).
- Vanno **sempre** private: dati sanitari, assicurazione, spese e saldi, prenotazioni e voli, alloggi prenotati. L'elenco aggiornato è in `_AI/scripts/vault_check.py` (`PRIVATE_REQUIRED`, `PRIVATE_CATEGORIES`, `PRIVATE_DIRS`).
- ⚠️ `publish: false` protegge **solo il sito**: il file resta leggibile su GitHub. **Mai** scrivere nel vault numeri di polizza, codici di prenotazione, documenti, telefoni o indirizzi personali. Usare un gestore esterno e scrivere solo "conferma salvata".
- Il Companion Excel si genera in `_private/` (ignorato da git) con `python3 _website/scripts/generate-companion-workbook.py`.

## Git

Flusso **Git Flow** (dettagli: `.agents/skills/git-flow-expert/SKILL.md`):
- si parte da `develop` (allineato a `main`) → `feature/<nome>` → merge in `develop` → release in `main`;
- **ogni push su `main` pubblica il sito** (GitHub Actions) → mai pushare su `main` senza conferma dell'utente;
- commit in italiano o semantici (`feat:`, `fix:`, `docs:`, `chore:`), mai riscrivere la storia di branch condivisi.

## Comandi

Non c'è un `package.json` in root: i comandi del sito si lanciano in `_website/`.

| Comando | Cosa fa |
|---|---|
| `python3 _AI/scripts/vault_check.py` | Verifica governance (link, frontmatter, privacy, fonte unica) |
| `cd _website && npm ci` | Installa le dipendenze (prima volta) |
| `cd _website && npm run sync` | Solo sync vault → contenuti Astro |
| `cd _website && npm run dev` | Sync + sito in sviluppo |
| `cd _website && npm run build` | Sync + build + indice di ricerca (come in CI) |

Obsidian CLI (opzionale, solo se Obsidian è aperto sul PC dell'utente): vedi `.agents/skills/obsidian-cli/SKILL.md`.

## Convenzioni del vault

| Convenzione | Significato |
|---|---|
| `[[wikilink]]` | Link interno Obsidian (non è un URL) |
| `#X/5` | Priorità luogo (5 = imperdibile, 1 = skip) |
| `//` in liste | Separatore di cluster geografico |
| `leaflet` / `mapview` | Mappe interattive (solo Obsidian) |
| `---` frontmatter | Metadati YAML (`type`, `destination`, `tags`, `last_updated`, `publish`) |
| `<!-- private -->…<!-- /private -->` | Contenuto escluso dal sito |

## Skill

Le skill sono in `.agents/skills/<nome>/SKILL.md`. Se l'harness non le carica da solo, **leggi il file della skill** quando il compito lo richiede.

| Skill | Quando usarla |
|---|---|
| `travel-vault-agent` | Sempre, per operare nel vault (struttura, template, contenuti) |
| `travel-web-research` | Ricerche web su prezzi, orari, ristoranti, trasporti |
| `git-flow-expert` | Branch, merge e rilasci |
| `obsidian-cli` | Interagire con Obsidian aperto (opzionale) |

## Compatibilità harness

| Harness | Come legge queste istruzioni |
|---|---|
| opencode | `opencode.jsonc` → `instructions: AGENTS.md + skill travel-vault-agent` |
| Claude Code | `CLAUDE.md` → importa `AGENTS.md` |
| Codex, Cursor, Copilot, Gemini e altri | leggono `AGENTS.md` direttamente |
| Antigravity / Windsurf | `.agent/workflows/update-knowledge.md` → rimanda qui |
