import { readdir, readFile, writeFile, mkdir, copyFile, stat, rm } from 'fs/promises';
import { join, dirname, basename, extname, relative, resolve } from 'path';
import { existsSync } from 'fs';
import { slug as sluggerSlug } from 'github-slugger';

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
  'Test per riferimento',
];

// Tipi frontmatter che NON vanno pubblicati come guide (ricerche web, note interne)
const EXCLUDED_TYPES = [
  'web_reference',
  'web_reference_note',
];

const URL_PREFIXES = {
  locations: '/Travel-Vault/locations/',
  info: '/Travel-Vault/guides/',
  itineraries: '/Travel-Vault/itineraries/',
};

let slugTypeMap = null;

async function buildSlugTypeMap() {
  const map = {};
  for (const { source, target } of SYNC_MAP) {
    const dir = join(VAULT_ROOT, source);
    const files = await findMarkdownFiles(dir);
    for (const file of files) {
      const slug = slugify(basename(file, '.md'));
      if (!map[slug]) map[slug] = target;
    }
  }
  slugTypeMap = map;
  return map;
}

function resolveWikilink(page, section) {
  // Page may be a full Obsidian path (e.g. "Locations/UnitedStates/NewYork/Attrazioni/Statua della Libertà").
  // We must resolve against the BASENAME slug, because slugs are generated from file basenames.
  const pageBase = page.split('/').pop();
  const slug = slugify(pageBase);
  const prefix = slugTypeMap?.[slug] ? URL_PREFIXES[slugTypeMap[slug]] : '/Travel-Vault/locations/';
  // Section anchors must match Astro's github-slugger heading IDs (keeps parens & accents).
  const sectionAnchor = section ? '#' + sluggerSlug(section.trim()) : '';
  return `${prefix}${slug}/${sectionAnchor}`;
}

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

function starsHtml(rating) {
  const full = parseInt(rating);
  if (isNaN(full) || full < 1 || full > 5) return '';
  const empty = 5 - full;
  return `<span class="rs" role="img" aria-label="${full}/5" title="${full}/5">${'★'.repeat(full)}${'☆'.repeat(empty)}</span>`;
}

function extractRating(content) {
  const ratings = [...content.matchAll(/#(\d)\/5/g)];
  if (ratings.length === 0) return null;
  const nums = ratings.map(r => parseInt(r[1]));
  return Math.max(...nums);
}

function transformContent(content, filePath) {
  let result = content;

  // Coordinate/rating extraction is only meaningful for location pages
  // (itineraries mention "#X/5" ratings of locations and must NOT get a rating).
  const isLocation = result.includes('type: location') || result.includes('type: city');

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

  // Extract highest rating from content
  const topRating = isLocation ? extractRating(result) : null;

  // Inject location and rating into frontmatter (only if not already present)
  const frontmatterLines = [];
  if (isLocation && lat && lon && !result.match(/^location:\s*/m)) frontmatterLines.push(`location: [${lat}, ${lon}]`);
  if (isLocation && topRating && !result.match(/^rating:\s*/m)) frontmatterLines.push(`rating: "${topRating}/5"`);

  if (frontmatterLines.length > 0) {
    const injection = '\n' + frontmatterLines.join('\n') + '\n';
    if (result.startsWith('---')) {
      const parts = result.split('---');
      if (parts.length >= 3) {
        parts[1] = parts[1] + injection;
        result = '---' + parts.slice(1).join('---');
      }
    }
  }

  // Transform cluster separators: // on its own line → visual divider
  result = result.replace(/^\/\/\s*$/gm, '<div class="cd"></div>');

  // Transform image embeds with optional size/alias: ![[image.jpg]] or ![[image.jpg|400]]
  result = result.replace(/!\[\[([^\]]+\.(jpg|jpeg|png|gif|webp|svg))(?:\|([^\]]*))?\]\]/gi, (_, imgName) => {
    return `![${imgName}](/Travel-Vault/images/vault/${imgName})`;
  });

  // Transform section-only in-page wikilinks: [[#Section|Display]] → [Display](#anchor)
  result = result.replace(/\[\[#([^\]|]+)\|([^\]]+)\]\]/g, (_, section, display) => {
    return `[${display}](#${sluggerSlug(section.trim())})`;
  });

  // Transform section-only in-page wikilinks: [[#Section]] → [Section](#anchor)
  result = result.replace(/\[\[#([^\]|]+)\]\]/g, (_, section) => {
    return `[${section}](#${sluggerSlug(section.trim())})`;
  });

  // Transform wikilinks with alias and optional section: [[Page#Section|Display]] → [Display](/prefix/slug/#section)
  result = result.replace(/\[\[([^\]|#]+)(?:#([^\]|]+))?\|([^\]]+)\]\]/g, (_, page, section, display) => {
    return `[${display}](${resolveWikilink(page, section)})`;
  });

  // Transform plain wikilinks with optional section: [[Page#Section]] → [Page](/prefix/slug/#section)
  result = result.replace(/\[\[([^\]|#]+)(?:#([^\]|]+))?\]\]/g, (_, page, section) => {
    return `[${page}](${resolveWikilink(page, section)})`;
  });

  // Remove orphaned Obsidian brackets left by malformed wikilinks in source (e.g. stray "]]")
  result = result.replace(/\]\]/g, '').replace(/\[\[/g, '');

  // Remove Obsidian comments: %% ... %%
  result = result.replace(/%%[\s\S]*?%%/g, '');

  // Remove TBLFM comments
  result = result.replace(/<!-- TBLFM:.*?-->/g, '');

  // Transform Obsidian ratings: #X/5 → visual stars HTML (after wikilinks to avoid conflicts)
  result = result.replace(/#(\d)\/5/g, (_, rating) => starsHtml(rating));

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

function hasExcludedType(content) {
  const typeMatch = content.match(/^type:\s*(\S+)/m);
  return typeMatch && EXCLUDED_TYPES.includes(typeMatch[1].replace(/['"]/g, ''));
}

async function sync() {
  console.log('Syncing vault content to Astro...\n');

  // Build slug → content type mapping for correct wikilink URL resolution
  await buildSlugTypeMap();

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
    const slugCounts = new Map();

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

      if (hasExcludedType(content)) {
        skipped++;
        continue;
      }

      const transformed = transformContent(content, filePath);
      let slugName = slugify(basename(filePath, '.md')) + '.md';
      const originalSlug = slugName;

      if (slugCounts.has(slugName)) {
        const count = slugCounts.get(slugName) + 1;
        slugCounts.set(slugName, count);
        slugName = slugName.replace(/\.md$/, `-${count}.md`);
        console.log(`  Duplicate slug resolved: "${originalSlug}" → "${slugName}" (from: ${filePath})`);
      } else {
        slugCounts.set(slugName, 0);
      }

      const outputPath = join(targetDir, slugName);
      await writeFile(outputPath, transformed, 'utf-8');
      count++;
    }

    console.log(`  ${source}/ -> ${target}/  (${count} files, ${skipped} skipped)`);
  }

  console.log('\nSync complete!\n');
}

sync().catch(console.error);
