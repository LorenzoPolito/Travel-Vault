// Aggiunge wikilink inline agli stop principali nel corpo dell'itinerario NYC
import { readFileSync, writeFileSync } from 'fs';

const path = 'C:/Users/loren/Documents/TravelBay/Travel-Vault/Itinerari/UnitedStates/NewYork/2026/New York - 21-29 Agosto 2026 - Itinerario Dettagliato.md';
let src = readFileSync(path, 'utf-8');

const map = [
  ['SoHo', '[[Locations/UnitedStates/NewYork/Quartieri/SoHo|SoHo]]'],
  ['Dominique Ansel Bakery', '[[Locations/UnitedStates/NewYork/Ristoranti/Dominique Ansel Bakery|Dominique Ansel Bakery]]'],
  ['Nolita', '[[Locations/UnitedStates/NewYork/Quartieri/Nolita|Nolita]]'],
  ['Washington Square Park', '[[Locations/UnitedStates/NewYork/Parchi/Washington Square Park|Washington Square Park]]'],
  ['Tompkins Square Park', '[[Locations/UnitedStates/NewYork/Parchi/Tompkins Square Park|Tompkins Square Park]]'],
  ["St. Mark's Place", "[[Locations/UnitedStates/NewYork/Attrazioni/St. Mark's Place|St. Mark's Place]]"],
  ['Astor Place', '[[Locations/UnitedStates/NewYork/Attrazioni/Astor Place|Astor Place]]'],
  ["Danny & Coop's", "[[Locations/UnitedStates/NewYork/Ristoranti/Danny & Coop's|Danny & Coop's]]"],
  ['Lower East Side', '[[Locations/UnitedStates/NewYork/Quartieri/Lower East Side|Lower East Side]]'],
  ["Katz's Delicatessen", "[[Locations/UnitedStates/NewYork/Ristoranti/Katzs Delicatessen|Katz's Delicatessen]]"],
  ['Williamsburg', '[[Locations/UnitedStates/NewYork/Quartieri/Williamsburg|Williamsburg]]'],
  ["L'Industrie Pizzeria", "[[Locations/UnitedStates/NewYork/Ristoranti/L'Industrie Pizzeria|L'Industrie Pizzeria]]"],
  ['Domino Park', '[[Locations/UnitedStates/NewYork/Parchi/Domino Park|Domino Park]]'],
  ['Roosevelt Island', '[[Locations/UnitedStates/NewYork/Attrazioni/Roosevelt Island|Roosevelt Island]]'],
  ['Grand Central Terminal', '[[Locations/UnitedStates/NewYork/Attrazioni/Grand Central Terminal|Grand Central Terminal]]'],
  ['Shake Shack', '[[Locations/UnitedStates/NewYork/Ristoranti/Shake Shack|Shake Shack]]'],
  ['Wall Street', '[[Locations/UnitedStates/NewYork/Attrazioni/Wall Street|Wall Street]]'],
  ['Red Hook', '[[Locations/UnitedStates/NewYork/Quartieri/Red Hook|Red Hook]]'],
  ['Hometown Bar-B-Que', '[[Locations/UnitedStates/NewYork/Ristoranti/Hometown BBQ|Hometown Bar-B-Que]]'],
  ['DUMBO', '[[Locations/UnitedStates/NewYork/Quartieri/DUMBO|DUMBO]]'],
  ['Brooklyn Bridge Park', '[[Locations/UnitedStates/NewYork/Parchi/Brooklyn Bridge Park|Brooklyn Bridge Park]]'],
  ['Brooklyn Bridge', '[[Locations/UnitedStates/NewYork/Attrazioni/Brooklyn Bridge|Brooklyn Bridge]]'],
  ['Central Park', '[[Locations/UnitedStates/NewYork/Parchi/Central Park|Central Park]]'],
  ['Levain Bakery', '[[Locations/UnitedStates/NewYork/Ristoranti/Levain Bakery|Levain Bakery]]'],
  ['American Museum of Natural History', '[[Locations/UnitedStates/NewYork/Museums/AMNH|AMNH]]'],
  ['Guggenheim Museum', '[[Locations/UnitedStates/NewYork/Museums/Guggenheim Museum|Guggenheim Museum]]'],
  ['Upper East Side', '[[Locations/UnitedStates/NewYork/Quartieri/Upper East Side|Upper East Side]]'],
  ['5th Avenue', '[[Locations/UnitedStates/NewYork/Attrazioni/5th Avenue|5th Avenue]]'],
  ["St. Patrick's Cathedral", "[[Locations/UnitedStates/NewYork/Attrazioni/St. Patrick's Cathedral|St. Patrick's Cathedral]]"],
  ['Rockefeller Center', '[[Locations/UnitedStates/NewYork/Attrazioni/Rockefeller Center|Rockefeller Center]]'],
  ['Radio City Music Hall', '[[Locations/UnitedStates/NewYork/Attrazioni/Radio City Music Hall|Radio City Music Hall]]'],
  ['Top of the Rock', '[[Locations/UnitedStates/NewYork/Grattacieli/Top of the Rock|Top of the Rock]]'],
  ['Keens Steakhouse', '[[Locations/UnitedStates/NewYork/Ristoranti/Keens Steakhouse|Keens Steakhouse]]'],
  ['New York Public Library', '[[Locations/UnitedStates/NewYork/Attrazioni/New York Public Library|New York Public Library]]'],
  ['Bryant Park', '[[Locations/UnitedStates/NewYork/Parchi/Bryant Park|Bryant Park]]'],
  ['Times Square', '[[Locations/UnitedStates/NewYork/Attrazioni/Times Square|Times Square]]'],
  ["Raising Cane's", "[[Locations/UnitedStates/NewYork/Ristoranti/Raising Canes|Raising Cane's]]"],
  ['Krispy Kreme', '[[Locations/UnitedStates/NewYork/Ristoranti/Krispy Kreme|Krispy Kreme]]'],
  ["McGee's Pub", "[[Locations/UnitedStates/NewYork/Ristoranti/McGeegs Pub|McGee's Pub]]"],
  ['Meatpacking District', '[[Locations/UnitedStates/NewYork/Quartieri/Meatpacking District|Meatpacking District]]'],
  ['Chelsea Market', '[[Locations/UnitedStates/NewYork/Attrazioni/Chelsea Market|Chelsea Market]]'],
  ['Pier 57', '[[Locations/UnitedStates/NewYork/Attrazioni/Pier 57|Pier 57]]'],
  ['Little Island', '[[Locations/UnitedStates/NewYork/Parchi/Little Island|Little Island]]'],
  ['High Line', '[[Locations/UnitedStates/NewYork/Parchi/High Line|High Line]]'],
  ['Hudson Yards', '[[Locations/UnitedStates/NewYork/Attrazioni/Hudson Yards|Hudson Yards]]'],
  ['Russ & Daughters', '[[Locations/UnitedStates/NewYork/Ristoranti/Russ & Daughters|Russ & Daughters]]'],
  ['Circle Line', '[[Locations/UnitedStates/NewYork/Attrazioni/Circle Line|Circle Line]]'],
  ['Empire State Building', '[[Locations/UnitedStates/NewYork/Grattacieli/Empire State Building|Empire State Building]]'],
  ['Union Square', '[[Locations/UnitedStates/NewYork/Attrazioni/Union Square|Union Square]]'],
  ['Unregular Pizza', '[[Locations/UnitedStates/NewYork/Ristoranti/Unregular Pizza|Unregular Pizza]]'],
  ['Flatiron Building', '[[Locations/UnitedStates/NewYork/Grattacieli/Flatiron Building|Flatiron Building]]'],
  ['Madison Square Park', '[[Locations/UnitedStates/NewYork/Parchi/Madison Square Park|Madison Square Park]]'],
  ['Madison Square Garden', '[[Locations/UnitedStates/NewYork/Attrazioni/Madison Square Garden|Madison Square Garden]]'],
  ['Chrysler Building', '[[Locations/UnitedStates/NewYork/Grattacieli/Chrysler Building|Chrysler Building]]'],
  ['7th Street Burger', '[[Locations/UnitedStates/NewYork/Ristoranti/7th Street Burger|7th Street Burger]]'],
  ['SUMMIT One Vanderbilt', '[[Locations/UnitedStates/NewYork/Grattacieli/SUMMIT One Vanderbilt|SUMMIT One Vanderbilt]]'],
  ['Statua della Libertà', '[[Locations/UnitedStates/NewYork/Attrazioni/Statua della Libertà|Statua della Libertà]]'],
  ['Ellis Island', '[[Locations/UnitedStates/NewYork/Attrazioni/Ellis Island|Ellis Island]]'],
  ['Battery Park', '[[Locations/UnitedStates/NewYork/Parchi/Battery Park|Battery Park]]'],
  ['World Trade Center', '[[Locations/UnitedStates/NewYork/Attrazioni/World Trade Center|World Trade Center]]'],
  ['9/11 Memorial', '[[Locations/UnitedStates/NewYork/Attrazioni/9-11 Memorial & Museum|9/11 Memorial]]'],
  ['Charging Bull', '[[Locations/UnitedStates/NewYork/Attrazioni/Charging Bull|Charging Bull]]'],
  ['Chinatown', '[[Locations/UnitedStates/NewYork/Quartieri/Chinatown|Chinatown]]'],
  ['Mei Lai Wah', '[[Locations/UnitedStates/NewYork/Ristoranti/Mei Lai Wah|Mei Lai Wah]]'],
  ['Fried Dumpling', '[[Locations/UnitedStates/NewYork/Ristoranti/Fried Dumpling|Fried Dumpling]]'],
  ['Little Italy', '[[Locations/UnitedStates/NewYork/Quartieri/Little Italy|Little Italy]]'],
  ['Prince Street Pizza', '[[Locations/UnitedStates/NewYork/Ristoranti/Prince Street Pizza|Prince Street Pizza]]'],
  ['Emily', '[[Locations/UnitedStates/NewYork/Ristoranti/Emily|Emily]]'],
  ['Greenwich Village', '[[Locations/UnitedStates/NewYork/Quartieri/Greenwich Village|Greenwich Village]]'],
  ['East Village', '[[Locations/UnitedStates/NewYork/Quartieri/East Village|East Village]]'],
  ['Chelsea', '[[Locations/UnitedStates/NewYork/Quartieri/Chelsea|Chelsea]]'],
  ['Financial District', '[[Locations/UnitedStates/NewYork/Quartieri/Financial District|Financial District]]'],
  ['Upper West Side', '[[Locations/UnitedStates/NewYork/Quartieri/Upper West Side|Upper West Side]]'],
];

// Ordina per lunghezza decrescente (nomi composti prima di quelli brevi)
map.sort((a, b) => b[0].length - a[0].length);

const cut = src.indexOf('## 📍 Pagine Correlate');
const body = src.slice(0, cut);
const tail = src.slice(cut);

// Elenco target già wikilinkati per evitare doppioni
const linkedTargets = new Set();
for (const m of body.matchAll(/\[\[Locations\/UnitedStates\/NewYork\/[^\]|]+/g)) {
  linkedTargets.add(m[0].replace('[[Locations/UnitedStates/NewYork/', ''));
}

let out = body;
let applied = 0;
for (const [name, link] of map) {
  // Se la pagina è già linkata altrove nel corpo, salta (evita link duplicati)
  if (linkedTargets.has(link.match(/Locations\/UnitedStates\/NewYork\/([^\]|]+)/)[1])) continue;

  // Proteggi i blocchi [[...]] esistenti sostituendoli con placeholder
  const placeholders = [];
  let tmp = out.replace(/\[\[[^\]]+\]\]/g, (m) => { placeholders.push(m); return `\u0000${placeholders.length - 1}\u0000`; });

  // Sostituisci il nome (parola intera) con il link, escludendo inside-heading-only
  const esc = name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const re = new RegExp(`\\b${esc}\\b`, 'g');
  const before = (tmp.match(new RegExp(`\\b${esc}\\b`, 'g')) || []).length;
  tmp = tmp.replace(re, link);
  const after = (tmp.match(new RegExp(`\\[\\[[^\\]]*\\|?${esc}[^\\]]*\\]\\]`, 'g')) || []).length;

  // Ripristina i placeholder
  tmp = tmp.replace(/\u0000(\d+)\u0000/g, (_, i) => placeholders[+i]);
  out = tmp;
  if (after > 0) applied++;
}

writeFileSync(path, out + tail, 'utf-8');
console.log(`Applicate sostituzioni su ${applied} luoghi (wikilink inline nel corpo).`);
