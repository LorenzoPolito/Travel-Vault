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
| Mappe | Leaflet con CartoDB dark |
| Ricerca | Pagefind (full-text) |
| Deploy | GitHub Actions → GitHub Pages |

## Struttura dei file

```
_website/
  src/
    constants.ts        ← ★ SINGLE SOURCE OF TRUTH
    data.ts             ← Data layer antifragile
    styles/global.css   ← Design system + utility classi
    layouts/Base.astro  ← Layout globale
    components/         ← Componenti atomici riutilizzabili
      Icon.astro        ← Sistema icone SVG
      Breadcrumbs.astro ← Breadcrumb navigazione
      EmptyState.astro  ← Stato vuoto
      Map.astro         ← Mappa Leaflet
      Search.astro      ← Ricerca Pagefind
    sections/           ← Sezioni di pagina autosufficienti
      HomeItineraries.astro
      HomeDestinations.astro
      HomeGuides.astro
      PageHeader.astro
    illustrations/      ← Illustrazioni SVG per nazioni/categorie
      CountryImage.astro
    pages/
      index.astro       ← Homepage
      404.astro
      sitemap.xml.ts
      destinations/
        index.astro     ← Lista destinazioni
        [dest]/
          index.astro   ← Dettaglio destinazione
      itineraries/
        index.astro     ← Lista itinerari
        [...slug].astro ← Dettaglio itinerario
      locations/
        [...slug].astro ← Dettaglio location
      guides/
        index.astro     ← Lista guide
        [...slug].astro ← Dettaglio guida
  public/
    robots.txt
    favicon.svg
    images/
      vault/            ← Immagini sincronizzate dal vault
      countries/        ← Illustrazioni SVG per nazioni
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

**Regola**: MAI hardcodare un path. Usa sempre `$(R.xxx(...))`.

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

- SI AUTOGESTISCE: se non ci sono dati, mostra `EmptyState` invece di rompersi
- SI NASCONDE: se la sezione non serve, semplicemente non la importi
- È PORTABILE: la stessa sezione può andare in qualsiasi pagina

## Illustrazioni per Nazioni

Le bento card (quando manca una cover image) mostrano:

1. **Illustrazione SVG della nazione** (es. torii per Giappone, colosseo per Italia)
2. **Fallback**: se l'SVG non esiste, gradient astratto con i colori della nazione
3. **Fallback finale**: gradient default scuro

Il mapping è in `src/illustrations/CountryImage.astro` + `constants.ts`.

## Icone SVG

Tutte le icone sono in `src/components/Icon.astro`. Nessuna emoji nel markup.

```astro
<Icon name="map" size={24} />
<Icon name="users" size={14} class="icon-tag" />
<Icon name="arrow-r" size={16} />
```

Icone disponibili: bag, map, book, globe, pin, compass, star, star-o, arrow-r, menu, users, coin, train, plane, shield, phone, ticket, city, temple, park, build, store, castle, hotel, food, active, info, search, link, heart, close, check, flag-jp, flag-it, flag-globe

## Design System (global.css)

### Variabili CSS

```css
--bg-primary: #0a0a0f    /* Sfondo principale */
--accent: #ff6b6b         /* Rosso accento */
--japan-gold: #f39c12     /* Oro per stelle rating */
--radius-lg: 16px         /* Border radius card */
--space-xl: 2rem          /* Spaziatura principale */
```

### Utility Classi

| Classe | Effetto |
|--------|---------|
| `.a--plain` | Rimuove sottolineatura link |
| `.page-header--flush` | Header senza bordo |
| `.mb-{lg,xl,2xl,3xl}` | Margin-bottom |
| `.mt-{lg,xl,2xl}` | Margin-top |
| `.text-gradient` | Testo con gradient accent |
| `.flex`, `.flex-col`, `.items-center` | Flexbox |
| `.gap-sm`, `.gap-md` | Gap |

### Breakpoint

| Nome | Larghezza | Target |
|------|-----------|--------|
| mobile | < 481px | Telefono |
| tablet | 481–768px | Tablet verticale |
| desktop-sm | 769–1023px | Tablet orizzontale |
| desktop | ≥ 1024px | Desktop |

## Regole per gli Agenti AI

1. MAI chiamare `getCollection()` direttamente — usa sempre `data.ts`
2. MAI hardcodare un URL — usa sempre `$(R.xxx(...))`
3. MAI usare emoji nel markup — usa `<Icon name="xxx" />`
4. OGNI sezione deve avere un EmptyState se i dati mancano
5. OGNI immagine deve avere un fallback (gradient, colore, testo)
6. NUOVE collection: aggiungi in `data.ts` + sezione in `sections/`
