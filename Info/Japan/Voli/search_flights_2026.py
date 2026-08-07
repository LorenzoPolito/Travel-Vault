"""Ricerca voli Giappone 2026 con dettagli completi per ogni volo.

Uso: python search_flights_details.py
Restituisce: compagnia, orari, durata totale, scali (città + minuti), per 1 adulto economy EUR.
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from google_flights import create_filter, FlightData, Passengers, get_flights_from_filter

MANUAL_CHECK = {"MU", "HU"}


def fmt_t(tt):
    h, m = divmod(tt or 0, 60)
    return f"{h}h{m:02d}"


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
                airlines = "/".join(sorted(set(fl.airline for fl in it.flights)))
                key = (price, airlines, it.travel_time)
                if key in seen:
                    continue
                seen.add(key)
                dep = f"{it.departure_time[0]:02d}:{it.departure_time[1]:02d}"
                arr = f"{it.arrival_time[0]:02d}:{it.arrival_time[1]:02d}"
                lay = []
                for lv in getattr(it, "layovers", []) or []:
                    m = getattr(lv, "minutes", None)
                    a = getattr(lv, "arrival_airport_city", None) or getattr(lv, "arrival_airport", None)
                    lay.append(f"{a} ({fmt_t(m)})")
                lay_txt = ", ".join(lay) if lay else "diretto"
                manual = any(a in MANUAL_CHECK for a in airlines.split("/")) or price <= 0
                note = " ⚠️verifica su Skyscanner" if manual else ""
                price_disp = "?" if manual else f"{price:.0f}€"
                results.append((float("inf") if manual else price, airlines, dep, arr, it.travel_time, lay_txt, note))
            except Exception:
                continue
        results.sort()
        shown = 0
        for price, a, dep, arr, dur, lay, note in results:
            print(f"  {price} | {a} | {dep}->{arr} | tot {fmt_t(dur)} | scalo/i: {lay}{note}")
            shown += 1
            if shown >= 10:
                break
        if shown == 0:
            print("  (prezzi non decodificabili)")
    except Exception as e:
        print(f"  ERRORE: {type(e).__name__}: {e}")


if __name__ == "__main__":
    for d in ["2026-10-27", "2026-10-29"]:
        search("FCO", "KIX", d, f"ANDATA {d}")
    for d in ["2026-11-07", "2026-11-08", "2026-11-09"]:
        search("TYO", "FCO", d, f"RITORNO TYO {d}")
