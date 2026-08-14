/**
 * bulk-download-nyc.mjs — Scarica le immagini Wikimedia per tutti i luoghi NYC
 * da citare nelle pagine. Scrive in allegati/ con prefisso nyc-<slug>-N.jpg
 */
import { execSync } from 'child_process';
import { dirname, resolve } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const WEBSITE_ROOT = resolve(__dirname, '..');

// [slug, search term, n immagini]
const PLACES = [
  ['quartiere-east-village', 'East Village Manhattan New York street'],
  ['quartiere-greenwich-village', 'Greenwich Village New York'],
  ['quartiere-williamsburg', 'Williamsburg Brooklyn New York'],
  ['quartiere-upper-east-side', 'Upper East Side Manhattan'],
  ['quartiere-meatpacking', 'Meatpacking District New York'],
  ['quartiere-little-italy', 'Little Italy Manhattan Mulberry Street'],
  ['quartiere-red-hook', 'Red Hook Brooklyn New York'],
  ['washingotn-square', 'Washington Square Park arch New York'],
  ['tompkins-square', 'Tompkins Square Park New York'],
  ['st-marks-place', "St. Mark's Place East Village New York"],
  ['astor-place', 'Astor Place cube New York'],
  ['roosevelt-island', 'Roosevelt Island tramway New York'],
  ['wall-street', 'Wall Street New York City'],
  ['charging-bull', 'Charging Bull Wall Street New York'],
  ['guggenheim', 'Guggenheim Museum New York'],
  ['5th-avenue', 'Fifth Avenue New York'],
  ['st-patricks-cathedral', 'St. Patricks Cathedral New York'],
  ['rockefeller-center', 'Rockefeller Center New York'],
  ['radio-city', 'Radio City Music Hall New York'],
  ['ny-public-library', 'New York Public Library Stephen A Schwarzman'],
  ['bryant-park', 'Bryant Park New York'],
  ['union-square', 'Union Square New York'],
  ['flatiron', 'Flatiron Building New York'],
  ['madison-square-park', 'Madison Square Park New York'],
  ['madison-square-garden', 'Madison Square Garden New York'],
  ['battery-park', 'Battery Park Manhattan'],
  ['world-trade-center', 'One World Trade Center Oculus New York'],
  ['little-island', 'Little Island New York Hudson River'],
  ['pier-57', 'Pier 57 New York'],
  ['domino-park', 'Domino Park Brooklyn'],
  ['nyc-city-hall', 'New York City Hall'],
  ['shake-shack', 'Shake Shack New York'],
  ['high-line', 'High Line New York park'],
  ['hudson-yards', 'Hudson Yards Vessel New York'],
  ['brooklyn-bridge-park', 'Brooklyn Bridge Park New York'],
  ['grand-central', 'Grand Central Terminal New York'],
  ['empire-state', 'Empire State Building New York'],
  ['summit-one-vanderbilt', 'SUMMIT One Vanderbilt New York'],
  ['top-of-the-rock', 'Top of the Rock Rockefeller Center'],
  ['times-square', 'Times Square New York night'],
  ['chelsea-market', 'Chelsea Market New York'],
  ['circle-line', 'Circle Line sightseeing cruise New York'],
  ['statua-liberta', 'Statue of Liberty New York'],
  ['ellis-island', 'Ellis Island New York'],
  ['brooklyn-bridge', 'Brooklyn Bridge New York'],
  ['9-11-memorial', '9 11 Memorial New York'],
  ['amnh', 'American Museum of Natural History New York'],
  ['met-museum', 'Metropolitan Museum of Art New York'],
  ['soho', 'SoHo New York cast iron architecture'],
  ['nolita', 'Nolita New York'],
  ['chinatown-nyc', 'Chinatown New York Mott Street'],
  ['financial-district', 'Financial District New York'],
  ['chelsea-nyc', 'Chelsea New York'],
  ['dumbo', 'DUMBO Brooklyn Manhattan Bridge view'],
  ['lower-east-side', 'Lower East Side New York'],
  ['upper-west-side', 'Upper West Side New York'],
];

const sleep = (ms) => new Promise(r => setTimeout(r, ms));

let ok = 0, fail = 0;
for (const [slug, term] of PLACES) {
  try {
    execSync(`node scripts/download-images.mjs "${term}" nyc-${slug} 3`, { stdio: 'inherit', cwd: WEBSITE_ROOT });
    ok++;
  } catch (e) {
    console.warn(`✗ ${slug} — ${e.message}`);
    fail++;
  }
  await sleep(3000);
}
console.log(`\nDownload completato: ${ok} ok, ${fail} fail`);
