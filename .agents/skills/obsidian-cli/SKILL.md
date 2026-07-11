---
name: obsidian-cli
description: Interagisci con il vault Obsidian tramite CLI. Usa quando devi cercare, leggere, creare, modificare note nel vault Obsidian. Richiede Obsidian in esecuzione con CLI attivato (Settings > General > Command line interface).
---

# Obsidian CLI Skill

Interagisci direttamente col vault Obsidian usando il CLI. Il vault attivo è `Travel-Vault`.

## Prerequisiti

1. Obsidian deve essere in esecuzione
2. CLI abilitato in Settings → General → Command line interface
3. CLI registrato nel PATH

## Comandi Disponibili

### Ricerca e Lettura

```
# Cerca nel vault
obsidian search query="itinerario giappone"

# Cerca in un vault specifico
obsidian search query="location: osaka" vault="Travel-Vault"

# Leggi un file specifico
obsidian read path="Itinerari/Japan/2026/Itinerario-Osaka-Hiroshima-Kyoto-Tokyo-dettagliato-(14notti)-24ott-7nov.md"

# Leggi file con formato JSON
obsidian read path="Locations/Japan/Lista dei Luoghi.md" format=json

# Elenca file recenti
obsidian files sort=modified limit=10
```

### Daily Note e Task

```
# Apri/Aggiungi oggi
obsidian daily

# Aggiungi task alla daily
obsidian daily:append content="- [ ] Prenotare volo Osaka 2026"

# Lista task dalla daily
obsidian tasks daily

# Aggiungi task con data
obsidian daily:append content="- [ ] Prenotare hotel Kyoto :: 2026-07-15"
```

### Creazione Note

```
# Crea nota da template
obsidian create name="Ristorante XYZ" template=Location

# Crea nota in cartella specifica
obsidian create name="Osaka-Giorno-3" path="Itinerari/Japan/2026/"
```

### Manutenzione Vault

```
# Trova link non risolti
obsidian unresolved

# Vedi tag con frequenza
obsidian tags counts

# Vedi statistiche vault
obsidian stats
```

### Uso in Workflow

Per ricerche complesse, combina più comandi:

```bash
# Trova tutte le location con rating 5/5
obsidian search query="#5/5" format=json

# Poi usa i risultati per creare una nota riassuntiva
obsidian create name="Top-Rated-Locations" content="Da completare"
```

## Note

- `obsidian help` — lista completa comandi
- `obsidian --tui` — modalità TUI interattiva con autocomplete
- Il vault root è `c:\Users\loren\Documents\TravelBay\Travel-Vault`
- Per headless sync (server): `obsidian sync:headless`
