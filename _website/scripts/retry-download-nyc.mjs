// Retry per i luoghi rimasti senza immagini (sequenziale, rispetta i rate limit)
import { execSync } from 'child_process';
import { dirname, resolve } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const WEBSITE_ROOT = resolve(__dirname, '..');
const sleep = (ms) => new Promise(r => setTimeout(r, ms));

const PLACES = [
  ['Chelsea Market New York', 'nyc-chelsea-market'],
  ['Circle Line cruise New York Harbor', 'nyc-circle-line'],
  ['SUMMIT One Vanderbilt New York', 'nyc-summit-one-vanderbilt'],
  ['World Trade Center Oculus New York', 'nyc-world-trade-center'],
  ['Little Island New York park', 'nyc-little-island'],
  ['Pier 57 New York Hudson River', 'nyc-pier-57'],
  ['Domino Park Brooklyn New York', 'nyc-domino-park'],
  ['Shake Shack New York', 'nyc-shake-shack'],
  ['Battery Park City New York', 'nyc-battery-park-city'],
  ['Nolita New York Elizabeth Street', 'nyc-nolita'],
  ['Chelsea Manhattan New York', 'nyc-chelsea-nyc'],
  ['Lower East Side New York Orchard Street', 'nyc-lower-east-side'],
  ['Upper West Side New York Broadway', 'nyc-upper-west-side'],
  ['Hudson Yards New York skyline', 'nyc-hudson-yards'],
];

for (const [term, slug] of PLACES) {
  try {
    execSync(`node scripts/download-images.mjs "${term}" ${slug} 3`, { stdio: 'inherit', cwd: WEBSITE_ROOT });
  } catch (e) {
    console.warn(`✗ ${slug}`);
  }
  await sleep(5000);
}
console.log('Finito');
