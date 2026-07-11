# Travel-Vault Website

Sito statico generato con **Astro 5** dal vault Obsidian Travel-Vault.

## Stack

- **Framework**: Astro 5
- **Mappe**: Leaflet (cartografia CartoDB dark)
- **Ricerca**: Pagefind (full-text search)
- **CI/CD**: GitHub Actions (deploy su push a `main`)

## Comandi

| Comando | Azione |
|---------|--------|
| `npm run dev` | Dev server su `localhost:4321` |
| `npm run build` | Build produzione in `dist/` |
| `npm run preview` | Preview build locale |

Il sync vault→sito avviene automaticamente in CI/CD. Per sync manuale:

```bash
node scripts/sync-content.mjs
```

## Struttura

```
src/
  pages/               ← Routes del sito
    index.astro        ← Homepage
    destinations/      ← Per destinazione
    itineraries/       ← Singoli itinerari
    locations/         ← Singole location
    guides/            ← Guide/info
  content/             ← Dati syncati dal vault (generati)
  components/          ← Componenti riutilizzabili
  layouts/             ← Layout condiviso
  styles/              ← CSS globale
scripts/
  sync-content.mjs     ← Script sync vault→Astro
```
