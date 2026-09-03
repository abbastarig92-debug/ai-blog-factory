import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import site from '../site.json';

export async function GET(context) {
  const posts = await getCollection('blog', ({ data }) => !data.draft);
  return rss({
    title: site.name,
    description: site.tagline,
    site: context.site,
    items: posts
      .sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf())
      .map((p) => ({
        title: p.data.title,
        description: p.data.description,
        pubDate: p.data.pubDate,
        link: `/blog/${p.slug}/`,
      })),
  });
}
