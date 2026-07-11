---
name: travel-web-research
description: Skill specializzata per ricerca web su viaggi, ristoranti, attrazioni e logistica. Usa quando devi cercare informazioni su ristoranti Michelin, orari di templi/attrazioni giapponesi, costi trasporti, meteo, eventi stagionali, e qualsiasi altra info pratica per la pianificazione del viaggio in Giappone.
---

# Travel Web Research Skill

Skill per ricerche web mirate alla pianificazione del viaggio in Giappone 2026.

## Siti di Riferimento

### Ristoranti e Cibo

| Sito | URL | Cosa Cercare |
|------|-----|--------------|
| Guida Michelin | https://guide.michelin.com/it/it | Ristoranti stellati e consigliati per città |
| Tabelog | https://tabelog.com | Recensioni ristoranti giapponesi (sistema打分 giapponese) |
| Gurunavi | https://www.gurunavi.com | Prenotazioni ristoranti, ricerca per zona |
| Ramen Database | https://ramendb.com | Classifica ramenya |

### Guide e Info Turistiche

| Sito | URL | Cosa Cercare |
|------|-----|--------------|
| GiapponePerTutti | https://www.giapponepertutti.it | Guida completa in italiano: trasporti, itinerari, cultura, costi |
| Japan-Guide | https://www.japan-guide.com | Guida turistica completa in inglese |
| Japan Travel | https://www.japan.travel | Sito ufficiale turismo giapponese |
| WikiTravel Japan | https://wikitravel.org/en/Japan | Guida collaborativa |

### Trasporti e Logistica

| Sito | URL | Cosa Cercare |
|------|-----|--------------|
| Hyperdia (via Japan Travel) | https://www.japan-travel.com/transport/ | Fasce orarie treni, costi |
| JR Pass | https://www.jrpass.com | Costi JR Pass e pass regionali |
| Google Maps | https://maps.google.com | Navigazione, orari, recensioni |
| Rome2Rio | https://www.rome2rio.com | Confronto trasporti multi-opzione |
| Klook | https://www.klook.com/it | Biglietti scontati attività, eSIM |
| Airalo | https://www.airalo.com | eSIM viaggio |

### Attrazioni e Prenotazioni

| Sito | URL | Cosa Cercare |
|------|-----|--------------|
| Klook Attività | https://www.klook.com/it/activity/ | Biglietti TeamLab, USJ, Harry Potter |
| USJ Official | https://www.usj.co.jp | Universal Studios Japan biglietti |
| TeamLab | https://www.teamlab.art | Mostre e biglietti |
| Lawson Ticket | https://l-tike.com | Biglietti attrazioni giapponesi |

### Meteo e Stagionalità

| Sito | URL | Cosa Cercare |
|------|-----|--------------|
| JMA | https://www.jma.go.jp | Meteo ufficiale Giappone |
| Weather News | https://weathernews.jp | Previsioni dettagliate |
| Japan Meteorological | https://www.data.jma.go.jp | Dati climatici storici per Ott/Nov |

### Eventi e Festival

| Sito | URL | Cosa Cercare |
|------|-----|--------------|
| Japan Travel Events | https://www.japan.travel/events/ | Festival e eventi |
| TimeOut Tokyo | https://www.timeout.com/tokyo | Eventi correnti a Tokyo |
| GoTokyo | https://www.gotokyo.org | Eventi e attrazioni Tokyo |

## Ricerche Tipiche

### Ricerca Ristoranti
```
webfetch: https://guide.michelin.com/it/it/ristoranti?city=OSAKA
webfetch: https://tabelog.com/tokyo/rstLst/
webfetch: https://www.giapponepertutti.it/category/mangiare-in-giappone/
```

### Ricerca Trasporti
```
webfetch: https://www.japan-guide.com/e/e2017.html  (IC Cards overview)
webfetch: https://www.jrpass.com/blog/jr-pass-vs-regional-passes
```

### Ricerca Orari Attrazioni
```
webfetch: https://www.japan-guide.com/e/e3901.html  (Kiyomizudera)
webfetch: https://www.teamlab.art/e/tokyo/
```

## Output Standard

Per ogni ricerca web, struttura il risultato in formato coerente:

```yaml
fonte: URL completo
data_ricerca: YYYY-MM-DD
info_principali:
  - punto 1
  - punto 2
dettagli: 
  orari: se applicabile
  costi: se applicabile
  prenotazione: necessario/non necessario/consigliato
note: annotazioni aggiuntive
```
