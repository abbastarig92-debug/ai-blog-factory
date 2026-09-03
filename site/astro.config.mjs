import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import site from './src/site.json' assert { type: 'json' };

export default defineConfig({
  site: site.url,
  integrations: [sitemap()],
  markdown: { shikiConfig: { theme: 'github-light' } },
  build: { inlineStylesheets: 'auto' },
});
