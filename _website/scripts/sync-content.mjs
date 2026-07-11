import { readdir, readFile, writeFile, mkdir, copyFile, stat, rm } from 'fs/promises';
import { join, dirname, basename, extname, relative, resolve } from 'path';
import { existsSync } from 'fs';

const VAULT_ROOT = resolve(dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Z]:)/, '$1')), '../..');
const WEBSITE_ROOT = resolve(dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Z]:)/, '$1')), '..');
const CONTENT_DIR = join(WEBSITE_ROOT, 'src', 'content');
const PUBLIC_IMAGES = join(WEBSITE_ROOT, 'public', 'images', 'vault');

const SYNC_MAP = [
  { source: 'Locations', target: 'locations' },
  { source: 'Itinerari', target: 'itineraries' },
  { source: 'Info', target: 'info' },
];

const IMAGE_EXTS = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'];

const EXCLUDED_FILES = [
  'senza-nome',
  'Senza nome',
  'Lista dei Luoghi',
  'lista-dei-luoghi',
];

function slugify(str) {
  return str
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[（(].*?[）)]/g, '')
    .replace(/[^\w\s-]/g, '')
    .replace(/[\s_]+/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '')
    .substring(0, 80);
}

function extractLeafletCoords(content) {
  const leafletMatch = content.match(/```leaflet\s*\n([\s\S]*?)```/);
  if (!leafletMatch) return null;

  const block = leafletMatch[1];
  const latMatch = block.match(/lat\s*:\s*(-?\d+\.\d+)/);
  const longMatch = block.match(/long\s*:\s*(-?\d+\.\d+)/);

  if (latMatch && longMatch) {
    return { lat: parseFloat(latMatch[1]), lon: parseFloat(longMatch[1]) };
  }
  return null;
}

function extractMapviewCoords(content) {
  const jsonMatch = content.match(/```mapview[\s\S]*?centerLat":\s*(-?\d+\.\d+)[\s\S]*?centerLng":\s*(-?\d+\.\d+)[\s\S]*?```/);
  if (jsonMatch) {
    return { lat: parseFloat(jsonMatch[1]), lon: parseFloat(jsonMatch[2]) };
  }
  return null;
}

function transformContent(content, filePath) {
  let result = content;

  const mapviewCoords = extractMapviewCoords(result);
  const leafletCoords = extractLeafletCoords(result);
  const gpsMatch = result.match(/^gps:\s*(-?\d+\.\d+),\s*(-?\d+\.\d+)/m);

  let lat, lon;
  if (mapviewCoords) {
    lat = mapviewCoords.lat;
    lon = mapviewCoords.lon;
  } else if (leafletCoords) {
    lat = leafletCoords.lat;
    lon = leafletCoords.lon;
  } else if (gpsMatch) {
    lat = parseFloat(gpsMatch[1]);
    lon = parseFloat(gpsMatch[2]);
  }

  // Remove mapview and leaflet code blocks
  result = result.replace(/```(mapview|leaflet)[\s\S]*?```/g, '');

  if (lat && lon && !result.match(/^location:\s*/m)) {
    if (result.startsWith('---')) {
      const parts = result.split('---');
      if (parts.length >= 3) {
        parts[1] = parts[1] + `location: [${lat}, ${lon}]\n`;
        result = '---' + parts.slice(1).join('---');
      }
    } else {
      result = `---\nlocation: [${lat}, ${lon}]\n---\n${result}`;
    }
  }

  // Transform image embeds with optional size/alias: ![[image.jpg]] or ![[image.jpg|400]]
  result = result.replace(/!\[\[([^\]]+\.(jpg|jpeg|png|gif|webp|svg))(?:\|([^\]]*))?\]\]/gi, (_, imgName) => {
    return `![${imgName}](/Travel-Vault/images/vault/${imgName})`;
  });

  // Transform wikilinks with alias: [[Page|Display]] → [Display](/Travel-Vault/locations/slug/)
  result = result.replace(/\[\[([^\]|]+)\|([^\]]+)\]\]/g, (_, page, display) => {
    const slug = slugify(page);
    return `[${display}](/Travel-Vault/locations/${slug}/)`;
  });

  // Transform plain wikilinks: [[Page Name (漢字)]] → [Page Name (漢字)](/Travel-Vault/locations/slug/)
  result = result.replace(/\[\[([^\]]+)\]\]/g, (_, page) => {
    const slug = slugify(page);
    return `[${page}](/Travel-Vault/locations/${slug}/)`;
  });

  // Remove Obsidian comments: %% ... %%
  result = result.replace(/%%[\s\S]*?%%/g, '');

  // Remove TBLFM comments
  result = result.replace(/<!-- TBLFM:.*?-->/g, '');

  return result;
}

async function findMarkdownFiles(dir) {
  const files = [];

  if (!existsSync(dir)) return files;

  const entries = await readdir(dir, { withFileTypes: true });

  for (const entry of entries) {
    const fullPath = join(dir, entry.name);
    if (entry.isDirectory()) {
      files.push(...await findMarkdownFiles(fullPath));
    } else if (entry.isFile() && extname(entry.name).toLowerCase() === '.md') {
      files.push(fullPath);
    }
  }

  return files;
}

async function syncImages() {
  const allegatDir = join(VAULT_ROOT, 'allegati');
  if (!existsSync(allegatDir)) {
    console.log('  \u{1F4C2} No allegati/ directory found, skipping images');
    return;
  }

  await mkdir(PUBLIC_IMAGES, { recursive: true });

  const entries = await readdir(allegatDir, { withFileTypes: true });
  let count = 0;

  for (const entry of entries) {
    if (entry.isFile()) {
      const ext = extname(entry.name).toLowerCase();
      if (IMAGE_EXTS.includes(ext)) {
        await copyFile(join(allegatDir, entry.name), join(PUBLIC_IMAGES, entry.name));
        count++;
      }
    }
  }

  console.log(`  \u{1F5BC}\uFE0F  Copied ${count} images from allegati/`);
}

function shouldExcludeFile(filePath) {
  const name = basename(filePath, '.md');
  return EXCLUDED_FILES.some(excluded =>
    name.toLowerCase() === excluded.toLowerCase()
  );
}

async function sync() {
  console.log('Syncing vault content to Astro...\n');

  await syncImages();

  for (const { source, target } of SYNC_MAP) {
    const sourceDir = join(VAULT_ROOT, source);
    const targetDir = join(CONTENT_DIR, target);

    if (!existsSync(sourceDir)) {
      console.log(`  Source directory not found: ${source}/`);
      continue;
    }

    if (existsSync(targetDir)) {
      const existingFiles = await readdir(targetDir, { withFileTypes: true });
      for (const file of existingFiles) {
        const fullPath = join(targetDir, file.name);
        if (file.isDirectory()) {
          await rm(fullPath, { recursive: true, force: true });
        } else {
          await rm(fullPath, { force: true });
        }
      }
    }
    await mkdir(targetDir, { recursive: true });

    const mdFiles = await findMarkdownFiles(sourceDir);
    let count = 0;
    let skipped = 0;
    const seenSlugs = new Map();

    for (const filePath of mdFiles) {
      if (shouldExcludeFile(filePath)) {
        skipped++;
        continue;
      }

      const content = await readFile(filePath, 'utf-8');

      if (!content.trim()) {
        skipped++;
        continue;
      }

      const transformed = transformContent(content, filePath);
      const slugName = slugify(basename(filePath, '.md')) + '.md';
      const outputPath = join(targetDir, slugName);

      if (seenSlugs.has(slugName)) {
        console.log(`  Duplicate slug: "${slugName}" from "${filePath}" and "${seenSlugs.get(slugName)}"`);
      }
      seenSlugs.set(slugName, filePath);

      await writeFile(outputPath, transformed, 'utf-8');
      count++;
    }

    console.log(`  ${source}/ -> ${target}/  (${count} files, ${skipped} skipped)`);
  }

  console.log('\nSync complete!\n');
}

sync().catch(console.error);
