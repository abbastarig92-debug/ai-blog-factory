import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    author: z.string().default('Editorial'),
    cluster: z.string().optional(),
    format: z.string().optional(),
    keyword: z.string().optional(),
    tags: z.array(z.string()).default([]),
    cover: z.string().optional(),
    ogTitle: z.string().optional(),
    keyTakeaway: z.string().optional(),
    faq: z.array(z.object({ q: z.string(), a: z.string() })).default([]),
    wordCount: z.number().optional(),
    affiliateLinks: z.array(z.string()).default([]),
    sources: z.array(z.object({ title: z.string().nullable(), url: z.string() })).default([]),
    draft: z.boolean().default(false),
  }),
});

export const collections = { blog };
