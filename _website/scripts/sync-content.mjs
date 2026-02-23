/**
 * sync-content.mjs
 * 
 * Syncs markdown content from the Obsidian vault into Astro's content collections.
 * Transforms wikilinks, image embeds, and removes Obsidian-specific blocks.
 * 
 * Run: node scripts/sync-content.mjs
 */

import { readdir, readFile, writeFile, mkdir, copyFile, stat, rm } from 'fs/promises';
import { join, dirname, basename, extname, relative, resolve } from 'path';
import { existsSync } from 'fs';

const VAULT_ROOT = resolve(dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Z]:)/, '$1')), '../..');
const WEBSITE_ROOT = resolve(dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Z]:)/, '$1')), '..');
const CONTENT_DIR = join(WEBSITE_ROOT, 'src', 'content');
const PUBLIC_IMAGES = join(WEBSITE_ROOT, 'public', 'images', 'vault');

// Directories to sync
const SYNC_MAP = [
  { source: 'Locations', target: 'locations' },
  { source: 'Itinerari', target: 'itineraries' },
  { source: 'Info', target: 'info' },
];

/**
 * Slugify a filename for URL-safe use
 */
function slugify(str) {
  return str
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '') // remove diacritics
    .replace(/[（(].*?[）)]/g, '')    // remove content in brackets
    .replace(/[^\w\s-]/g, '')        // remove special chars
    .replace(/[\s_]+/g, '-')         // spaces/underscores → hyphens
    .replace(/-+/g, '-')             // collapse multiple hyphens
    .replace(/^-|-$/g, '')           // trim leading/trailing hyphens
    .substring(0, 80);               // limit length
}

/**
 * Transform Obsidian-flavored markdown to standard markdown
 */
function transformContent(content, filePath) {
  let result = content;

  // Extract coordinate from mapview (JSON format) or manual format
  const mapviewJsonMatch = result.match(/```mapview[\s\S]*?centerLat":\s*(-?\d+\.\d+)[\s\S]*?centerLng":\s*(-?\d+\.\d+)[\s\S]*?```/);
  const gpsMatch = result.match(/^gps:\s*(-?\d+\.\d+),\s*(-?\d+\.\d+)/m);
  
  let lat, lon;
  if (mapviewJsonMatch) {
    lat = parseFloat(mapviewJsonMatch[1]);
    lon = parseFloat(mapviewJsonMatch[2]);
  } else if (gpsMatch) {
    lat = parseFloat(gpsMatch[1]);
    lon = parseFloat(gpsMatch[2]);
  }

  // Remove mapview and leaflet code blocks before further processing
  result = result.replace(/```(mapview|leaflet)[\s\S]*?```/g, '');

  if (lat && lon && !result.match(/^location:\s*/m)) {
    // Insert into existing frontmatter
    if (result.startsWith('---')) {
      const parts = result.split('---');
      if (parts.length >= 3) {
        parts[1] = parts[1] + `location: [${lat}, ${lon}]\n`;
        result = '---' + parts.slice(1).join('---');
      }
    } else {
      // Create new frontmatter if missing
      result = `---\nlocation: [${lat}, ${lon}]\n---\n${result}`;
    }
  }

  // Transform image embeds: ![[image.jpg]] → ![image](/images/vault/image.jpg)
  result = result.replace(/!\[\[([^\]]+\.(jpg|jpeg|png|gif|webp|svg))\]\]/gi, (_, imgName) => {
    return `![${imgName}](/Travel-Vault/images/vault/${imgName})`;
  });

  // Transform wikilinks with alias: [[Page|Display]] → [Display](/Travel-Vault/locations/page)
  result = result.replace(/\[\[([^\]|]+)\|([^\]]+)\]\]/g, (_, page, display) => {
    const slug = slugify(page);
    return `[${display}](/Travel-Vault/locations/${slug}/)`;
  });

  // Transform plain wikilinks: [[Page Name (漢字)]] → [Page Name (漢字)](/Travel-Vault/locations/page-name)
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

/**
 * Recursively find all .md files in a directory
 */
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

/**
 * Find and copy image files from allegati/
 */
async function syncImages() {
  const allegatDir = join(VAULT_ROOT, 'allegati');
  if (!existsSync(allegatDir)) {
    console.log('  📂 No allegati/ directory found, skipping images');
    return;
  }

  await mkdir(PUBLIC_IMAGES, { recursive: true });

  const entries = await readdir(allegatDir, { withFileTypes: true });
  let count = 0;

  for (const entry of entries) {
    if (entry.isFile()) {
      const ext = extname(entry.name).toLowerCase();
      if (['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'].includes(ext)) {
        await copyFile(join(allegatDir, entry.name), join(PUBLIC_IMAGES, entry.name));
        count++;
      }
    }
  }

  console.log(`  🖼️  Copied ${count} images from allegati/`);
}

/**
 * Main sync function
 */
async function sync() {
  console.log('🔄 Syncing vault content to Astro...\n');

  // Sync images first
  await syncImages();

  // Sync each content directory
  for (const { source, target } of SYNC_MAP) {
    const sourceDir = join(VAULT_ROOT, source);
    const targetDir = join(CONTENT_DIR, target);

    if (!existsSync(sourceDir)) {
      console.log(`  ⚠️  Source directory not found: ${source}/`);
      continue;
    }

    // Clean target directory if exists
    if (existsSync(targetDir)) {
      const existingFiles = await readdir(targetDir, { withFileTypes: true });
      for (const file of existingFiles) {
        const fullPath = join(targetDir, file.name);
        if (file.isDirectory()) {
          // Recursive delete for safety (though we flatten now)
          await rm(fullPath, { recursive: true, force: true });
        } else {
          await rm(fullPath, { force: true });
        }
      }
    }
    await mkdir(targetDir, { recursive: true });

    const mdFiles = await findMarkdownFiles(sourceDir);
    let count = 0;

    for (const filePath of mdFiles) {
      const content = await readFile(filePath, 'utf-8');
      const transformed = transformContent(content, filePath);

      // Create a meaningful output path - FLATTENED for reliable wikilinks
      const sluggedName = slugify(basename(filePath, '.md')) + '.md';
      
      const outputPath = join(targetDir, sluggedName);
      await writeFile(outputPath, transformed, 'utf-8');
      count++;
    }

    console.log(`  ✅ ${source}/ → ${target}/  (${count} files)`);
  }

  console.log('\n✨ Sync complete!\n');
}

sync().catch(console.error);
