---
type: info
destination: Japan
category: metodologia
tags:
  - guide
  - best-practice
  - itinerario
  - workflow
  - template
---

# Come Creare un Itinerario di Viaggio — Best Practice

Questo documento descrive la metodologia usata per creare l'itinerario del Giappone 2026. Ogni passo è replicabile per qualsiasi destinazione.

---

## 1. Fase di Ricerca

### 1.1 Raccolta dati iniziale
Prima di scrivere una riga di itinerario, raccogliere:
- **Date e durata** del viaggio
- **Persone** coinvolte e loro esigenze (allergie, mobilità, interessi)
- **Budget** indicativo totale e per persona
- **Città/base** di partenza e ritorno

### 1.2 Fact-checking
**Regola fondamentale: non supporre mai. Ogni informazione va verificata.**
- Orari di apertura → Japan-Guide, sito ufficiale
- Costi trasporti → JR Pass, Rome2Rio, siti ufficiali
- Meteo → Japan Meteorological Agency (JMA)
- Ristoranti → Tabelog, Google Maps, Michelin Guide
- Voli → Rome2Rio per range prezzi, Skyscanner per alert

### 1.3 Fonti consigliate

| Fonte | Cosa cercare |
|---|---|
| japan-guide.com | Orari, costi, trasporti, food guide |
| rome2rio.com | Voli, tratte, range prezzi |
| tabelog.com | Ristoranti locali (3.5+ = buono) |
| jma.go.jp | Meteo ufficiale Giappone |
| google.com/maps | Recensioni, orari, foto |
| skyscanner.net | Alert voli |

---

## 2. Struttura dell'Itinerario

### 2.1 Formato consigliato
L'itinerario segue questa struttura gerarchica:

```
# Nome Viaggio
  ## Riepilogo Tappe (tabella città/giorni/notti)
  ## Info Generali (fuso, valuta, IC card, eSIM, assicurazione)
  ## Trasporti (tabella tratte + decisione JR Pass)
  ## Legenda (simboli: 🟢🟡🔵⚪🅿)
  ## Budget Giornaliero (tabella giorni)
  ## Alloggi (tabella con cucina ✅❌)
  # ITINERARIO
    ## Giorno 1 — Data
      **Difficoltà** **Budget** **Meteo**
      Attività divise per cluster geografici
      **Cibo — Alternative** (🅰️🅱️🅲🅳)
      Piano B (🅿)
  ## Monitoraggio Voli (calendario check)
  ## Budget Tracker (stima vs reale)
  ## Budget Totale
  ## Booking Checklist
```

### 2.2 Ogni giorno deve avere:
| Elemento | Formato |
|---|---|
| Data + giorno settimana | `## Giorno 2 — Domenica 25 Ottobre` |
| Difficoltà | `**Difficoltà:** 2/4` |
| Budget giorno | `**Budget:** ~37 €` |
| Meteo | `**Meteo:** 18–23°C, 30% pioggia (fonte)` |
| Cluster geografico | `### Mattina | Cluster Nord` |
| Orari attrazioni | `(9:00–17:00, ¥500)` |
| Piano B | `🅿 **PIANO B (pioggia):** ...` |
| Cibo alternative | `🅰️ ... 🅱️ ... 🅲 ... 🅳` |
| Note Rebecca/allergie | `⚠️ **Rebecca:** ...` |

### 2.3 Convenzioni di scrittura
- **[[Wikilink]]** per tutti i luoghi menzionati (link interno Obsidian)
- **#X/5** per rating (5=must, 1=skip)
- **//** per separare cluster geografici
- **🅰️🅱️🅲🅳** per alternative cibo
- **⚠️ Rebecca:** per note allergie (se applicabile)
- **🅿 PIANO B** per ogni giorno

---

## 3. Gestione Allergie Alimentari

### 3.1 Informazioni da raccogliere subito
- **Lista completa** degli allergeni
- **Gravità** (leggera/moderata/grave — con o senza adrenaline?)
- **Cosa è sicuro mangiare** in ogni tipo di ristorante
- **Catene sicure** (es. Saizeriya per soia-free)

### 3.2 Documenti da preparare
- **Cartellino in lingua locale** (stampato + plastificato)
- **Frasi utili** per ordinare
- **Lista supermarket** con indirizzi vicino a ogni alloggio

### 3.3 Alloggi
- **VERIFICARE** che TUTTI gli alloggi abbiano cucina/angolo cottura
- Creare una pagina per ogni alloggio con tabella servizi
- Verificare supermarket raggiungibile a piedi

---

## 4. Cibo: Strategia Raccomandazioni

### 4.1 Piramide delle raccomandazioni

```
                ⭐ Michelin (1 sola volta)
               🔵 Bib Gourmand (qualità-prezzo)
              🟢 Kaitenzushi, Ramen, Gyudon (catene)
             🟡 Mercati e Street Food
            🟠 Konbini e Supermarket
```

### 4.2 Per ogni giorno, offrire
- 🅰️ Opzione street food/locale
- 🅱️ Opzione Bib Gourmand o catena
- 🅲 Opzione seduti/izakaya
- 🅳 Opzione Rebecca (se applicabile)
- Prezzo per ogni opzione

---

## 5. Budget Tracking

### 5.1 Struttura budget
```
| Voce | Stima | Reale | Delta | Note |
```

### 5.2 Monitoraggio voli
- Calendario check ogni 2 giorni
- Colonne: Data, Stato, Andata, Ritorno, TOT A/R, Fonti
- Link verificati alle fonti

---

## 6. Fact-checking: Checklist Pre-Publicazione

Prima di considerare un itinerario completo:

- [ ] Orari di apertura verificati su fonte ufficiale
- [ ] Costi trasporti verificati (JR Pass, biglietti singoli)
- [ ] Meteo verificato (dati JMA o equivalente)
- [ ] Ristoranti: nome, zona, prezzo, tipo verificati
- [ ] Alloggi: cucina, indirizzo, servizi verificati
- [ ] Voli: range prezzi con fonte
- [ ] Ogni giorno ha un Piano B
- [ ] Ogni pasto ha alternative per ogni commensale
- [ ] [[Wikilink]] funzionanti per tutti i luoghi
- [ ] Assicurazione viaggio consigliata con costi
- [ ] Cartellino allergie stampabile

---

## 7. Template per Nuova Destinazione

Copia questa struttura per una nuova destinazione:

```markdown
---
type: itinerario
destination: [Paese]
durata_giorni: X
durata_notti: X
data_partenza: "YYYY-MM-DD"
data_ritorno: "YYYY-MM-DD"
status: pianificato
autori:
  - Persona1
  - Persona2
percorso: "Città1 → Città2 → Città3"
budget_totale_stimato: "X €/persona"
tags:
  - itinerario
  - [paese]
  - [anno]
  - attivo
---

# [Viaggio] — [Date]

[Tratte] · X giorni / Y notti

## Riepilogo Tappe
| Tappa | Giorni | Notti | Date |
|:---|:---:|:---:|:---|

## Info Generali
| Info | Dettaglio |
|---|---|

## Trasporti
| Tratta | Mezzo | Tempo | Costo | Copertura |
|---|---|---|---|---|

## Legenda
## Budget Giornaliero
## Alloggi
## Monitoraggio
## Budget Tracker
## Budget Totale
## Booking Checklist
```

---

## 8. Errori Comuni da Evitare

| Errore | Soluzione |
|---|---|
| **Inventare ristoranti** | Solo fonti verificate. Se non trovi, scrivi "cercare su Google Maps" |
| **Ignorare allergie** | Chiedere SEMPRE. Documentare per ogni pasto |
| **Nessun Piano B** | Ogni giorno deve avere alternativa meteo/costi/chiusure |
| **Troppi stellati Michelin** | 1 al massimo per viaggio. Preferire Bib Gourmand |
| **Date non verificate** | Controllare festività nazionali e chiusure settimanali |
| **Mancanza di fonti** | Ogni dato deve avere una fonte verificabile |
| **[[Wikilink]] rotti** | Controllare che ogni link punti a un file esistente |
