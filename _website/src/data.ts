/**
 * @@ DATA LAYER ANTIFRAGILE @@
 *
 * Ogni accesso alle collection è safe-wrapped: se una collection manca,
 * restituisce array vuoto invece di crashare. Usa sempre i metodi di
 * questo file invece di chiamare getCollection() direttamente.
 *
 * ## Come aggiungere una nuova collection:
 * 1. Aggiungi il nome all'array COLLECTIONS qui sotto
 * 2. Crea una funzione getXxx() che chiama getSafe('xxx')
 * 3. Se serve dati derivati, aggiungi una funzione qui sotto
 *
 * ## Perché non chiamare getCollection() direttamente?
 * - Se il nome della collection cambia, lo cambi in UN posto solo
 * - Se la collection non esiste, NON crasha il build
 * - I dati derivati sono calcolati una volta e riutilizzati
 */
import { getCollection } from 'astro:content';
import { ACTIVE_ITIN_PREFIX } from './constants';

/* ─── Collection registry ─────────────────────────── */
// Aggiungi qui le tue collection. Il resto del sito si adatta.
export const COLLECTIONS = [
  'locations',
  'itineraries',
  'info',
] as const;

export type CollectionName = (typeof COLLECTIONS)[number];

/* ─── Safe access ─────────────────────────────────── */
async function getSafe(name: CollectionName) {
  try {
    const entries = await getCollection(name);
    return entries ?? [];
  } catch (e) {
    console.warn(`[data] Collection "${name}" non trovata — restituisco []`);
    return [];
  }
}

/* ─── Public API ──────────────────────────────────── */
export async function getLocations() {
  return getSafe('locations');
}

export async function getItineraries() {
  return getSafe('itineraries');
}

export async function getInfo() {
  return getSafe('info');
}

/* ─── Derived data ────────────────────────────────── */

/** Set di destinazioni uniche da locations + itinerari */
export async function getDestinations() {
  const [loc, itin] = await Promise.all([getLocations(), getItineraries()]);
  const set = new Set<string>();
  loc.forEach((l: any) => { if (l.data?.destination) set.add(l.data.destination); });
  itin.forEach((i: any) => { if (i.data?.destination) set.add(i.data.destination); });
  return [...set];
}

/** Tutte le city */
export async function getCities() {
  const loc = await getLocations();
  return loc.filter((l: any) => l.data?.type === 'city');
}

/** Statistiche generali (numeri) */
export async function getStats() {
  const [loc, itin, info] = await Promise.all([
    getLocations(),
    getItineraries(),
    getInfo(),
  ]);
  return {
    locations: loc.length,
    itineraries: itin.length,
    info: info.length,
    cities: loc.filter((l: any) => l.data?.type === 'city').length,
  };
}

/** Itinerario attivo (quello col prefissato ACTIVE_ITIN_PREFIX) */
export async function getActiveItinerary() {
  const itin = await getItineraries();
  return itin.find((i: any) => i.id.startsWith(ACTIVE_ITIN_PREFIX)) ?? null;
}

/** Itinerari non attivi */
export async function getOtherItineraries() {
  const [all, active] = await Promise.all([getItineraries(), getActiveItinerary()]);
  return active ? all.filter((i: any) => i !== active) : all;
}

/** Filtra locations per destinazione */
export async function getLocationsByDest(dest: string) {
  const loc = await getLocations();
  return loc.filter((l: any) => l.data?.destination === dest);
}

/** Filtra itinerari per destinazione */
export async function getItinerariesByDest(dest: string) {
  const itin = await getItineraries();
  return itin.filter((i: any) => i.data?.destination === dest);
}

/** Filtra info per destinazione */
export async function getInfoByDest(dest: string) {
  const info = await getInfo();
  return info.filter((e: any) => e.data?.destination === dest);
}
