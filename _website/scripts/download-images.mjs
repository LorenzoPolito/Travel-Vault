/**
 * download-images.mjs — Scarica immagini da Wikimedia Commons in allegati/
 *
 * Uso:
 *   node scripts/download-images.mjs "Statue of Liberty New York" nyc-statua-liberta 3
 *
 * Cerca le prime N immagini su Wikimedia Commons per il termine, scarica le
 * thumbnails (~960px) nella cartella `allegati/` del vault con prefisso del nome.
 * Gli screenshot vengono poi sincronizzati dal vault al sito (public/images/vault).
 */
import { mkdir, writeFile } from 'fs/promises';
import { join, dirname, resolve } from 'path';
import { fileURLToPath } from 'url';

const SCRIPT_DIR = dirname(fileURLToPath(import.meta.url));
const VAULT_ROOT = resolve(SCRIPT_DIR, '../..');
const ALLEGATI = join(VAULT_ROOT, 'allegati');
const API = 'https://commons.wikimedia.org/w/api.php';
const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36 Travel-Vault-sync';

const [,, searchTerm, prefix = 'nyc', count = 3] = process.argv;
const n = parseInt(count, 10) || 3;

const sleep = (ms) => new Promise(r => setTimeout(r, ms));

async function api(params) {
  const url = `${API}?${new URLSearchParams({ format: 'json', origin: '*', ...params })}`;
  const res = await fetch(url, { headers: { 'User-Agent': UA } });
  if (!res.ok) throw new Error(`API ${res.status}`);
  return res.json();
}

async function searchImages(term, limit) {
  const data = await api({
    action: 'query',
    generator: 'search',
    gsrsearch: term,
    gsrnamespace: '6',
    gsrlimit: String(limit),
    prop: 'imageinfo',
    iiprop: 'url|size|mime',
    iiurlwidth: '960',
  });
  const pages = data?.query?.pages;
  if (!pages) return [];
  return Object.values(pages)
    .map(p => p?.imageinfo?.[0])
    .filter(meta => meta && (meta.thumburl || meta.url))
    .map(meta => {
      const mime = meta.mime || '';
      let ext = mime.split('/')[1];
      if (ext === 'jpeg') ext = 'jpg';
      const url = (meta.thumburl || meta.url || '').split('?')[0];
      return { url, ext: ext || 'jpg' };
    });
}

function sanitize(name) {
  return name.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
}

await mkdir(ALLEGATI, { recursive: true });
let images = [];
for (let attempt = 1; attempt <= 3; attempt++) {
  try {
    images = await searchImages(searchTerm, n * 2);
    break;
  } catch (e) {
    if (attempt < 3) await sleep(attempt * 3000);
    else { console.error(`Errore API per "${searchTerm}": ${e.message}`); process.exit(1); }
  }
}

if (images.length === 0) {
  console.error(`Nessuna immagine trovata per "${searchTerm}"`);
  process.exit(1);
}

let saved = 0;
for (let i = 0; i < images.length && saved < n; i++) {
  const img = images[i];
  const filename = `${sanitize(prefix)}-${saved + 1}.${img.ext}`;
  const outPath = join(ALLEGATI, filename);
  for (let attempt = 1; attempt <= 4; attempt++) {
    try {
      const res = await fetch(img.url, { headers: { 'User-Agent': UA } });
      if (!res.ok) { console.warn(`  retry(${attempt}) ${img.url} -> ${res.status}`); await sleep(3000 * attempt); continue; }
      const buf = Buffer.from(await res.arrayBuffer());
      if (buf.length < 2000) { console.warn(`  retry(${attempt}) too small ${buf.length}`); await sleep(2000); continue; }
      await writeFile(outPath, buf);
      console.log(`  ✓ ${filename} (${(buf.length / 1024).toFixed(0)} KB)`);
      saved++;
      break;
    } catch (e) {
      console.warn(`  retry(${attempt}) ${e.message}`);
      await sleep(3000 * attempt);
    }
  }
  await sleep(800);
}

console.log(`\nSalvate ${saved} immagini in allegati/ per "${searchTerm}"`);
