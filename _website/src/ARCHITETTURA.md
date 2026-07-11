# Architettura del Sito — Travel-Vault Website

## Filosofia

**Antifragile** — il sistema migliora nel caos. Ogni componente:

- Assume che i dati possano mancare → **fallisce in graceful degradation**
- Assume che le collection possano cambiare → **si adatta automaticamente**
- Assume che le rotte possano essere modificate → **usa un route system centralizzato**

## Stack

| Layer | Tecnologia |
|-------|-----------|
| Framework | Astro 5 (static) |
| CSS | Variabili + utility classi (nessun framework) |
| Icone | SVG inline via `Icon.astro` (30+ icone) |
| Ricerca | Pagefind (full-text) |
| Deploy | GitHub Actions → GitHub Pages |

## Struttura dei file

```
_website/
  src/
    constants.ts        ← ★ SINGLE SOURCE OF TRUTH
    data.ts             ← Data layer antifragile
    ARCHITETTURA.md     ← Questa documentazione
    styles/
      global.css        ← Design system + utility classi + componenti
    layouts/
      Base.astro        ← Layout globale (nav, footer, search, meta)
    components/         ← Componenti atomici riutilizzabili
      Icon.astro        ← Sistema icone SVG (30+ icone)
      Breadcrumbs.astro ← Breadcrumb navigazione con aria-label
      EmptyState.astro  ← Stato vuoto universale (si adatta a qualsiasi contesto)
      Search.astro      ← Ricerca Pagefind (full-text)
    sections/           ← Sezioni di pagina autosufficienti
      HomeItineraries.astro  ← Sezione itinerari homepage
      HomeDestinations.astro ← Sezione destinazioni homepage
      HomeGuides.astro       ← Sezione guide homepage
    illustrations/      ← Illustrazioni SVG per nazioni e topic
      CountryImage.astro ← Immagine nazione (fallback via onerror)
      TopicImage.astro   ← Immagine topic guida (match per keyword)
    pages/
      index.astro       ← Homepage (usa sections/)
      404.astro         ← Pagina 404 con nav + CTA
      sitemap.xml.ts    ← Sitemap dinamico (tutte le 132+ pagine)
      destinations/
        index.astro     ← Lista destinazioni
        [dest]/
          index.astro   ← Dettaglio destinazione (città, luoghi, itinerari)
      itineraries/
        index.astro     ← Lista itinerari
        [...slug].astro ← Dettaglio itinerario (split layout, day nav, route)
      locations/
        [...slug].astro ← Dettaglio location (rating, info)
      guides/
        index.astro     ← Lista guide
        [...slug].astro ← Dettaglio guida
  public/
    robots.txt          ← SEO
    favicon.svg         ← Favicon
    images/
      vault/            ← Immagini sincronizzate dal vault (sync-content.mjs)
      countries/        ← Illustrazioni SVG per nazioni
        japan.svg       ← Torii + Fuji + sakura
        italia.svg      ← Colosseo + cipresso
        default.svg     ← Bussola
      topics/           ← Illustrazioni SVG per topic guide
        transport.svg   ← Shinkansen
        safety.svg      ← Shield con check
        flights.svg     ← Aereo in volo
        esim.svg        ← Telefono con segnale
        pass.svg        ← Biglietto con barcode
        guide.svg       ← Libro con segnalibro
```

## Sistema Rotte (constants.ts)

TUTTI i path del sito sono generati dalle funzioni in `R`:

```ts
import { R, url } from '../constants';
const $ = (p: string) => url(base, p);

// Uso:
<a href={$(R.destination('japan'))}>Giappone</a>
<a href={$(R.itinerary(activeItin.id))}>Itinerario</a>
```

**Regola**: MAI hardcodare un URL. Usa sempre `$(R.xxx(...))`.

### Rotte disponibili

| Funzione | Path generato | Esempio |
|----------|-------------|---------|
| `R.home` | `/` | — |
| `R.destinations` | `/destinations/` | — |
| `R.destination(slug)` | `/destinations/{slug}/` | `japan/` |
| `R.itineraries` | `/itineraries/` | — |
| `R.itinerary(slug)` | `/itineraries/{slug}/` | `itinerario-giappone/` |
| `R.guides` | `/guides/` | — |
| `R.guide(slug)` | `/guides/{slug}/` | `ic-cards/` |
| `R.location(slug)` | `/locations/{slug}/` | `dotonbori/` |
| `R.image(filename)` | `/images/vault/{filename}` | `foto.jpg` |
| `R.countryImage(filename)` | `/images/countries/{filename}` | `japan.svg` |

## Data Layer (data.ts)

TUTTE le pagine importano i dati da `data.ts`, MAI da `getCollection()` diretto.

```ts
import { getLocations, getItineraries, getInfo, getStats } from '../data';
```

### Vantaggi

1. **Safe access**: se una collection non esiste, restituisce `[]` invece di crashare
2. **Registry centralizzato**: in `COLLECTIONS` nell'array in alto
3. **Derived data**: funzioni come `getDestinations()`, `getActiveItinerary()`, `getStats()` evitano duplicazione
4. **Future-proof**: aggiungi una collection in UN file solo (`data.ts`)

### Come aggiungere una nuova collection

```ts
// 1. In data.ts — aggiungi alla registry
export const COLLECTIONS = ['locations', 'itineraries', 'info', 'nuova'] as const;

// 2. In data.ts — aggiungi safe access
export async function getNuova() { return getSafe('nuova'); }

// 3. In sections/ — crea NuovaSection.astro
// 4. In index.astro — importa e usa
```

## Sezioni Component (sections/)

Ogni sezione della homepage è un componente indipendente che:

- **SI AUTOGESTISCE**: se non ci sono dati, mostra `EmptyState` invece di rompersi
- **SI NASCONDE**: se non la importi, semplicemente non appare
- **È PORTABILE**: la stessa sezione può andare in qualsiasi pagina
- **RICEVE PROPS**: ogni sezione riceve solo ciò che gli serve via `Props`

### Sezioni disponibili

| Componente | Mostra | Si nasconde se |
|-----------|--------|---------------|
| `HomeItineraries` | Featured + bento card | Nessun itinerario |
| `HomeDestinations` | Card destinazioni | Nessuna destinazione |
| `HomeGuides` | Card guide con TopicImage | Nessuna guida |

## Navigazione Giorni (Itinerario Detail)

La sidebar dell'itinerario mostra i link ai giorni tramite **JavaScript scrollIntoView**:

```ts
// Cliccando su un giorno, cerca l'heading per testo e scrolla
headings.querySelector('h2')?.textContent === 'Giorno 1 — ...'
```

**Perché JavaScript invece di href="#anchor"?**
Astro genera ID per gli heading con un algoritmo diverso da `slugify()`. Usando JavaScript, la navigazione funziona SEMPRE indipendentemente da come Astro genera gli ID.

## Illustrazioni

### CountryImage (per nazioni)

Usato nelle **bento card** degli itinerari (quando manca cover image).

```
┌─────────────────┐
│  [SVG nazione]  │  ← CountryImage (opacity 0.35, oggetto cover)
│  gradient sfondo │
│  ─────────────  │
│  città → città  │  ← testo
│  [durata]       │
└─────────────────┘
```

**Registry**: `src/illustrations/CountryImage.astro` (mappa `dest` → filename SVG)

**Antifragile**: `onerror="this.style.display='none'"` — se SVG manca, non si vede.

### TopicImage (per guide)

Usato nelle **card guida** come sfondo decorativo.

**Registry**: `src/illustrations/TopicImage.astro` (match per keyword nella categoria)

```ts
const TOPIC_RULES = [
  { keywords: ['trasport', 'train', 'bus', 'treno'], file: 'transport.svg' },
  { keywords: ['sicur', 'safety', 'sicurezza'], file: 'safety.svg' },
  // ...
];
```

## Destination Themes (constants.ts)

Ogni nazione ha un tema visuale unico:

```ts
export const DEST_THEMES = {
  japan: { gradient: 'linear-gradient(...)', accent: '#ff6b6b' },
  italia: { gradient: 'linear-gradient(...)', accent: '#58d68d' },
};
export function getDestTheme(dest: string): DestTheme;
```

**Aggiungere una nazione**: crea `public/images/countries/{slug}.svg` + aggiungi a `DEST_THEMES`.

## Design System

### Variabili CSS (in global.css)

```css
--bg-primary: #0a0a0f      /* Sfondo principale */
--bg-card: #1a1a28         /* Sfondo card */
--accent: #ff6b6b          /* Rosso accento */
--japan-gold: #f39c12      /* Oro per stelle rating */
--font-body: "Inter", ...  /* Font principale */
--font-display: "Outfit"  /* Font titoli */
--radius-lg: 16px          /* Border radius card */
--space-xl: 2rem           /* Spaziatura principale */
```

### Utility Classi

| Classe | Effetto |
|--------|---------|
| `.a--plain` | Link senza sottolineatura |
| `.page-header--flush` | Header senza bordo |
| `.mb-{lg,xl,2xl,3xl}` | Margin-bottom |
| `.mt-{lg,xl,2xl}` | Margin-top |
| `.text-gradient` | Testo con gradient accent |
| `.flex`, `.flex-col`, `.items-center` | Flexbox helper |
| `.gap-sm`, `.gap-md` | Gap helper |
| `.w-full` | Larghezza 100% |
| `.a--plain` | Text-decoration none |

### Breakpoint

| Nome | Larghezza | Target |
|------|-----------|--------|
| mobile-xs | < 481px | Telefono piccolo |
| mobile | 481–768px | Telefono/tablet verticale |
| tablet | 769–1023px | Tablet orizzontale |
| desktop | ≥ 1024px | Desktop |

## Icone SVG (Icon.astro)

Tutte le icone sono in `src/components/Icon.astro` come SVG inline.

```astro
<Icon name="map" size={24} />
<Icon name="users" size={14} class="icon-tag" />
<Icon name="arrow-r" size={16} />
```

**Icone disponibili**: bag, map, book, globe, pin, compass, star, star-o, arrow-r, menu, chevron-r, users, coin, train, plane, shield, phone, ticket, city, temple, park, build, store, castle, hotel, food, quarter, street, active, info, alert, search, link, heart, sun, moon, close, check, external, flag-jp, flag-it, flag-globe

## Sync Script (scripts/sync-content.mjs)

Trasforma il vault Obsidian in content Astro:

1. **Coordinate**: estrae da block `leaflet`/`mapview` o frontmatter `gps:` → frontmatter `location: [lat, lng]`
2. **Rating**: estrae `#X/5` dal contenuto → frontmatter `rating: "X/5"` + HTML stelle
3. **Cluster**: trasforma `//` in `<div class="cd">` (divisore cluster)
4. **Wikilink**: converte `[[Page]]` → `[Page](/Travel-Vault/locations/slug/)`
5. **Immagini**: `![[file.jpg]]` → `![file.jpg](/Travel-Vault/images/vault/file.jpg)`
6. **Duplicate handling**: slug duplicati → append `-1`, `-2` (antifragile)

## Regole per Agenti AI

1. MAI chiamare `getCollection()` direttamente — usa sempre `data.ts`
2. MAI hardcodare un URL — usa sempre `$(R.xxx(...))`
3. MAI usare emoji nel markup — usa `<Icon name="xxx" />`
4. OGNI sezione deve avere un EmptyState se i dati mancano
5. OGNI immagine deve avere un fallback (gradient, colore, onerror hide)
6. NUOVE collection: aggiungi in `data.ts` + sezione in `sections/`
7. NUOVE nazioni: SVG in `public/images/countries/` + `DEST_THEMES` in `constants.ts`
8. NUOVI topic: SVG in `public/images/topics/` + `TOPIC_RULES` in `TopicImage.astro`
9. Per scroll a elementi nella pagina: usa JavaScript `scrollIntoView` (non href="#id")
