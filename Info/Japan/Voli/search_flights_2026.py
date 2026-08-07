"""Ricerca voli Giappone 2026 — FCO->KIX e ritorni, via Google Flights API (libreria google-flights).

Uso: python search_flights_2026.py

Note:
- Restituisce prezzi per 1 adulto, economy, EUR.
- China Eastern (MU): Google non espone il prezzo via API (bug noto) -> segnalato,
  verificare su Skyscanner/Trip.com.
- Nessun browser: usa l'endpoint interno di Google Flights (veloce, ~3s/ricerca).
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from google_flights import create_filter, FlightData, Passengers, get_flights_from_filter

# Compagnie note per non decodificare i prezzi via API (verifica manuale consigliata)
MANUAL_CHECK = {"MU", "HU"}


def search(origin, dest, date, label):
    print(f"\n=== {label}: {origin} -> {dest} {date} (1 pax) ===")
    try:
        f = create_filter(
            flight_data=[FlightData(date=date, from_airport=[origin], to_airport=[dest])],
            trip="one-way",
            passengers=Passengers(adults=1),
            seat="economy",
        )
        res = get_flights_from_filter(f, currency="EUR", language="it-IT")
        items = list(res.best or []) + list(res.other or [])
        if not items:
            print("  (nessun risultato)")
            return
        results = []
        seen = set()
        for it in items:
            try:
                price = it.itinerary_summary.price
                stops = len(it.flights) - 1
                airlines = "/".join(sorted(set(fl.airline for fl in it.flights)))
                dep = f"{it.departure_time[0]:02d}:{it.departure_time[1]:02d}" if it.departure_time else "?"
                arr = f"{it.arrival_time[0]:02d}:{it.arrival_time[1]:02d}" if it.arrival_time else "?"
                key = (price, stops, airlines)
                if key in seen:
                    continue
                seen.add(key)
                # MU/HU: price 0 (non esposto) -> segnala
                if price <= 0 or any(a in MANUAL_CHECK for a in airlines.split("/")):
                    results.append((float("inf"), stops, airlines, dep, arr, it.travel_time, "VERIFICA SU SKYSCANNER"))
                else:
                    results.append((price, stops, airlines, dep, arr, it.travel_time, ""))
            except Exception:
                continue
        results.sort()
        shown = 0
        for price, stops, a, dep, arr, dur, note in results:
            tag = " ⚠️" if note else ""
            note_txt = f" [{note}]" if note else ""
            if note:
                print(f"  ?EUR | {stops} scalo | {a} | {dep}->{arr} | {dur}min{tag}{note_txt}")
            else:
                print(f"  {price:.0f}EUR | {stops} scalo | {a} | {dep}->{arr} | {dur}min{tag}")
            shown += 1
            if shown >= 8:
                break
        if shown == 0:
            print("  (prezzi non decodificabili — controllare su Skyscanner)")
    except Exception as e:
        print(f"  ERRORE: {type(e).__name__}: {e}")


if __name__ == "__main__":
    # ANDATE
    for d in ["2026-10-26", "2026-10-27", "2026-10-28", "2026-10-29"]:
        search("FCO", "KIX", d, f"ANDATA {d}")
    # RITORNI da Tokyo (TYO = HND/NRT)
    for d in ["2026-11-05", "2026-11-06", "2026-11-07", "2026-11-08", "2026-11-09"]:
        search("TYO", "FCO", d, f"RITORNO TYO {d}")
