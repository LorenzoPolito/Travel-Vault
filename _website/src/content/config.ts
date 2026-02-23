import { defineCollection, z } from 'astro:content';

const locations = defineCollection({
  type: 'content',
  schema: z.object({
    type: z.string().optional(),
    category: z.string().optional(),
    destination: z.string().optional(),
    city: z.string().optional(),
    rating: z.string().optional(),
    orari: z.string().optional(),
    costo: z.string().optional(),
    durata_visita: z.string().optional(),
    location: z.array(z.number()).or(z.string()).optional(),
    gps: z.string().optional(),
    locations: z.array(z.string()).optional(),
    tags: z.array(z.string()).optional(),
  }),
});

const itineraries = defineCollection({
  type: 'content',
  schema: z.object({
    type: z.string().optional(),
    destination: z.string().optional(),
    durata: z.string().optional(),
    durata_giorni: z.number().optional(),
    durata_notti: z.number().optional(),
    data_partenza: z.string().optional(),
    data_ritorno: z.string().optional(),
    status: z.string().optional(),
    autori: z.array(z.string()).optional(),
    percorso: z.string().optional(),
    budget_totale_stimato: z.string().optional(),
    tags: z.array(z.string()).optional(),
  }),
});

const info = defineCollection({
  type: 'content',
  schema: z.object({
    type: z.string().optional(),
    destination: z.string().optional(),
    category: z.string().optional(),
    categoria: z.string().optional(),
    tags: z.array(z.string()).optional(),
  }),
});

export const collections = { locations, itineraries, info };
