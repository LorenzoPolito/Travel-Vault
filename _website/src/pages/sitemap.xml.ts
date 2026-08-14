import { getCollection } from 'astro:content';
import { destSlug } from '../constants';

export async function GET() {
  const locations = await getCollection('locations');
  const itineraries = await getCollection('itineraries');
  const info = await getCollection('info');

  const siteUrl = 'https://lorenzopolito.github.io/Travel-Vault';

  const pages: string[] = [
    `${siteUrl}/`,
    `${siteUrl}/destinations/`,
    `${siteUrl}/itineraries/`,
    `${siteUrl}/guides/`,
  ];

  const dests = new Set<string>();
  locations.forEach((l: any) => { if (l.data?.destination) dests.add(l.data.destination); });
  itineraries.forEach((i: any) => { if (i.data?.destination) dests.add(i.data.destination); });
  dests.forEach((d: string) => pages.push(`${siteUrl}/destinations/${destSlug(d)}/`));

  itineraries.forEach((i: any) => {
    const slug = i.id.replace(/\.md$/, '');
    pages.push(`${siteUrl}/itineraries/${slug}/`);
  });

  locations.forEach((l: any) => {
    const slug = l.id.replace(/\.md$/, '');
    pages.push(`${siteUrl}/locations/${slug}/`);
  });

  info.forEach((i: any) => {
    const slug = i.id.split('/').pop()?.replace(/\.md$/, '');
    if (slug) pages.push(`${siteUrl}/guides/${slug}/`);
  });

  const uniquePages = [...new Set(pages)];

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${uniquePages.map(url => `  <url><loc>${url}</loc></url>`).join('\n')}
</urlset>`;

  return new Response(xml, {
    status: 200,
    headers: { 'Content-Type': 'application/xml' },
  });
}
