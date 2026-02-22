# Travel-Vault — Metadati Workspace

> Generato il: 2026-02-23
> Aggiornato da: Antigravity AI Agent

---

## Descrizione

**Travel-Vault** è un vault [Obsidian](https://obsidian.md/) per la **pianificazione di viaggi in generale**.
Attualmente contiene principalmente contenuto sul **Giappone**, ma copre anche altri viaggi (es. Calabria 2025).

**Autori principali:** Lorenzo, Damiano  
**Strumento:** Obsidian (con plugin Leaflet, Kanban, git)  
**Versioning:** Git attivo sulla root

---

## Struttura delle Cartelle

| Cartella | Descrizione |
|---|---|
| `Itinerari/` | Itinerari di viaggio, organizzati per destinazione e durata |
| `Locations/` | Schede sui luoghi, categorizzate per tipo |
| `Info/` | Informazioni logistiche (trasporti, pass, sicurezza) |
| `Documenti Esterni/` | PDF e DOCX importati da fonti esterne |
| `allegati/` | Immagini, foto e allegati vari |
| `_AI/` | (questa cartella) Knowledge e tools per agenti AI |
| `.obsidian/` | Configurazione Obsidian (non modificare) |

---

## Destinazioni Coperte

| Destinazione | Stato | Note |
|---|---|---|
| 🇯🇵 Giappone | **Principale / In evoluzione** | Contenuto molto ricco (itinerari, location, info) |
| 🇮🇹 Calabria | **Archiviato** | Itinerario Parghelia 2025 (23-31 Ago 2025) completato |

---

## Convenzioni del Vault

### Wikilink
I `[[wikilink]]` connettono note internamente. Il nome dentro le parentesi corrisponde esattamente al nome file (senza `.md`).

### Sistema di Punteggio Location
`#X/5` indica la **priorità/interesse** di un luogo:
- `#5/5` = Assolutamente da visitare
- `#4/5` = Molto consigliato
- `#3/5` = Interessante
- `#2/5` = Opzionale
- `#1/5` = Bassa priorità / da fare solo se si ha tempo

### Cluster Geografici
Il separatore `//` nelle liste di luoghi separa **cluster geografici**: gruppi di luoghi vicini tra loro, raggiungibili a piedi o in metro in ~30 minuti (a Tokyo il tempo può essere maggiore per via delle dimensioni della città).

### Tag YAML
Le note città usano frontmatter YAML con:
```yaml
locations:
  - NomeCittà
tags:
  - city
  - map
```

### Mappe
Le city notes contengono blocchi `leaflet` per mappe interattive in Obsidian. Alcune usano anche `mapview`.

### Kanban
Il file `Itinerario Kanban Template.md` è un template Kanban (plugin Obsidian) per organizzare pasti per giorno.

---

## Tecnologie Obsidian Usate

| Plugin | Uso |
|---|---|
| Leaflet | Mappe interattive embedded nelle note città |
| Kanban | Template per organizzazione giornaliera pasti |
| Table (nativo) | Tabelle per sintesi itinerari e budget |
| Callout (>) | Blocchi di evidenziazione (info, consigli, note) |
| Wikilinks (nativo) | Navigazione interna tra note |

---

## Note per Agenti AI

- **Non esiste un "itinerario definitivo"** — tutti gli itinerari sono varianti di lavoro in evoluzione.
- **L'itinerario più recente e completo** per il Giappone è `Itinerari/Japan/Solo con i luoghi/14 giorni/Itinerario Tokyo-Kyoto-Osaka-Hiroshima-Tokyo(14 giorni)(15feb-1mar).md` (creato da Lorenzo e Damiano), ma potrebbe non essere quello adottato.
- **Le schede città** (es. `Locations/Japan/Cities/Tokyo(東京).md`) spesso contengono contenuto informativo estratto da siti turistici (japan.travel, giapponepertutti.it) e link alle mappe.
- **Gli hotel** sono linkati tramite `magictravel.ai` nelle note città di Kyoto e Osaka, ma non c'è una sezione prenotazioni centralizzata.
- **La `Lista dei Luoghi.md`** in `Locations/Japan/` è il punto di riferimento master per tutti i luoghi con voti e cluster.
