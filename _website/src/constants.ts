export const SITE = {
  name: 'Travel-Vault',
  description: 'Organizza i tuoi viaggi con Travel-Vault',
  lang: 'it' as const,
  url: 'https://lorenzopolito.github.io/Travel-Vault',
  favicon: '/favicon.svg',
  author: 'Travel-Vault',
}

export const NAV = [
  { label: 'Home', href: '/' },
  { label: 'Destinazioni', href: '/destinations/' },
  { label: 'Itinerari', href: '/itineraries/' },
  { label: 'Guide', href: '/guides/' },
] as const

export const DEST_EMOJI: Record<string, string> = {
  japan: '🇯🇵',
  giappone: '🇯🇵',
  italia: '🇮🇹',
}

export const TYPE_EMOJI: Record<string, string> = {
  city: '🏙️',
  quartiere: '🏘️',
  street: '🛤️',
  location: '📍',
}

export const CAT_EMOJI: Record<string, string> = {
  templ: '⛩️',
  park: '🌳',
  build: '🏢',
  store: '🛍️',
  castle: '🏯',
  hotel: '🏨',
  restaurant: '🍜',
}

export const GUIDE_CAT_EMOJI: Record<string, string> = {
  trasport: '🚄',
  'ic-card': '🚄',
  sicur: '🛡️',
  safety: '🛡️',
  vol: '✈️',
  'e-sim': '📱',
  sim: '📱',
  pass: '🎫',
}

export const PRETTY_NAMES: Record<string, string> = {
  'itinerario-giappone-24ott-7nov2026': 'Giappone 2026 — 24 Ott · 7 Nov',
}

export const ACTIVE_ITIN_PREFIX = 'itinerario-giappone-24ott'

export function slugToName(slug: string): string {
  const name = slug.split('/').pop() || ''
  return name
    .replace(/-/g, ' ')
    .replace(/\.md$/, '')
    .replace(/\b\w/g, (l: string) => l.toUpperCase())
}

export function getDestinationEmoji(dest: string): string {
  return DEST_EMOJI[dest.toLowerCase()] || '🌍'
}

export function getTypeEmoji(type: string | undefined | null): string {
  if (!type) return '📍'
  return TYPE_EMOJI[type.toLowerCase()] || '📍'
}

export function getCategoryEmoji(cat: string): string {
  const lower = cat.toLowerCase()
  for (const [key, emoji] of Object.entries(CAT_EMOJI)) {
    if (lower.includes(key)) return emoji
  }
  return '📍'
}

export function getGuideCategoryEmoji(cat: string): string {
  const lower = cat.toLowerCase()
  for (const [key, emoji] of Object.entries(GUIDE_CAT_EMOJI)) {
    if (lower.includes(key)) return emoji
  }
  return '📖'
}

export function starsFromRating(rating: string): string {
  const m = rating.match(/(\d+)\/?\d*/)
  if (!m) return ''
  const n = parseInt(m[1])
  if (n < 1 || n > 5) return ''
  return '★'.repeat(n) + '☆'.repeat(5 - n)
}

export function extractCoverImage(body: string): string | null {
  const match = body.match(/!\[.*?\]\((.*?)\)/)
  return match ? match[1] : null
}

/* --- Destination Themes --- */
// Usato dalle bento card per mostrare gradienti unici per ogni nazione.
// Aggiungi una nuova nazione qui + la sua illustrazione SVG in public/images/countries/.
export interface DestTheme {
  gradient: string;
  accent: string;
}

export const DEST_THEMES: Record<string, DestTheme> = {
  japan: {
    gradient: 'linear-gradient(135deg, #1a0a2e 0%, #16213e 40%, #0f3460 100%)',
    accent: '#ff6b6b',
  },
  italia: {
    gradient: 'linear-gradient(135deg, #0d1b0d 0%, #1a2e1a 40%, #0d1b2a 100%)',
    accent: '#58d68d',
  },
};

export function getDestTheme(dest: string): DestTheme {
  return DEST_THEMES[dest.toLowerCase()] || {
    gradient: 'linear-gradient(135deg, #1a1a2e 0%, #2d1b2e 40%, #1a1a3e 100%)',
    accent: '#ffa07a',
  };
}

/* --- Atomic Route System --- */
// Path definitions: single source of truth for all URLs.
// Always use the named functions; never hardcode paths.
const stripMd = (s: string) => s.replace(/\.md$/, '')
const stripMdSlash = (s: string) => `${stripMd(s)}/`

export const R = {
  home: '/',
  destinations: '/destinations/',
  destination: (slug: string) => `/destinations/${slug}/`,
  itineraries: '/itineraries/',
  itinerary: (slug: string) => `/itineraries/${stripMdSlash(slug)}`,
  locations: '/locations/',
  location: (slug: string) => `/locations/${stripMdSlash(slug)}`,
  guides: '/guides/',
  guide: (slug: string) => `/guides/${stripMdSlash(slug)}`,
  image: (filename: string) => `/images/vault/${encodeURIComponent(filename)}`,
  countryImage: (filename: string) => `/images/countries/${encodeURIComponent(filename)}`,
  assets: (path: string) => `/_assets/${path}`,
  favicon: SITE.favicon,
}

/** Resolve a route path with the site's base URL.
 *  First arg is from `import.meta.env.BASE_URL` (in Astro) or a known base.
 *  Second arg is a path from `R.*`.
 */
export function url(base: string, path: string): string {
  const p = path.startsWith('/') ? path : `/${path}`
  return `${base}${p}`
}
