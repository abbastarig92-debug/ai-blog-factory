---
title: How to Generate Consistent Characters in Midjourney v6
slug: generate-consistent-characters-midjourney-v6
description: Learn how to generate consistent characters in Midjourney v6. Lock facial
  identity, swap outfits, and build narrative scenes using the --cref parameter.
pubDate: '2026-09-17T17:57:07+00:00'
updatedDate: '2026-09-17T17:57:07+00:00'
author: ToolStack Lab Editorial
cluster: image-ai
format: how-to
keyword: how to generate consistent characters in midjourney v6
tags:
- midjourney v6
- ai art
- character consistency
- prompt engineering
- midjourney cref
cover: /covers/generate-consistent-characters-midjourney-v6.svg
ogTitle: 'Midjourney v6 Consistent Characters: The Complete --cref Guide'
keyTakeaway: Lower your character weight with --cw to preserve facial identity while
  freely swapping outfits and environments.
faq:
- q: What is the difference between high and low --cw in Midjourney v6?
  a: High character weight locks facial structure, hair, and clothing for continuous
    shots. Low character weight locks only facial identity, letting you change the
    character's clothing, hairstyle, or setting.
wordCount: 1571
affiliateLinks: []
sources:
- title: How to Create Consistent Characters in Midjourney V6!
  url: https://www.youtube.com/watch?v=Vi5KQUZSKkM
- title: Midjourney Consistent Character Creation - V6 - Step By Step Tutorial
  url: https://www.youtube.com/watch?v=ug9InWREELg
- title: Generating Consistent Characters in the Midjourney Web Interface - Experiencing
    Elearning
  url: https://christytuckerlearning.com/generating-consistent-characters-in-the-midjourney-web-interface
- title: My Steps for VERY Consistent Midjourney Characters!
  url: https://www.youtube.com/watch?v=2JVvGZd6Kx4
- title: Medium
  url: https://medium.com/@tridibghosh/consistent-characters-in-midjourney-v6-easy-peasy-6c79f5dd5675
- title: 'How to Create Consistent Characters in Midjourney: The Complete Guide for
    2026'
  url: https://medium.com/@impijushsaha/how-to-create-consistent-characters-in-midjourney-the-complete-guide-for-2026-405c3bfbb4e1
- title: How To Create Consistent Characters In Midjourney 2026 ( Step By Step)
  url: https://www.youtube.com/watch?v=rDL7GrzLuGE
- title: Creating Consistent Characters with MidJourney Version 6
  url: https://medium.com/@deeznotes77/creating-consistent-characters-with-midjourney-version-6-introducing-cref-cw-7dbae1d9d793
draft: true
---

## Quick Start: The --cref and --cw Syntax for Midjourney v6

To help **generate consistent characters in midjourney v6**, you can use two parameters: `--cref` (Character Reference) and `--cw` (Character Weight). Passing an image URL into `--cref` prompts Midjourney to map facial features and anatomy onto your new image prompt.

```text
[prompt description] --cref [URL] --cw [weight]
```

Here is a ready-to-use production prompt:

```text
photo of an Asian woman with black hair, running through a rain-slicked city street at night, cinematic lighting --cref https://cdn.discordapp.com/attachments/1234/5678/anchor.png --cw [weight]
```

Consider these parameter guidelines depending on your shot requirements:

*   **Higher Character Weight:** Locks the character's face, hair texture, and clothing outfit. Use this for continuous scenes where wardrobe changes are not desired.
*   **Lower Character Weight:** Locks primarily the facial identity. Use this when swapping wardrobe, hairstyles, or historical eras.

---

## Step 1: How to Generate Consistent Characters in Midjourney v6 with Master Anchor Images

Your character's consistency depends heavily on the anchor image you feed into `--cref`. If your reference image has heavy shadows, motion blur, or complex background clutter, Midjourney will replicate those artifacts across every subsequent generation.

Start by rendering a clean, neutral anchor image. Use front-facing angles, even lighting, and simple attire.

```text
photo of an Asian woman with black hair, black eyes, and tan skin, wearing a neutral white t-shirt, studio lighting, plain background, neutral facial expression
```

Once you render an image you like, retrieve the direct image link:

1.  **Discord Workflow:** Click the rendered image to expand it, right-click, select **Copy Link**, and ensure the URL ends in `.png`, `.jpg`, or `.webp`. Alternatively, react to the message with an envelope emoji (✉️) to receive the seed number and direct media links in your Midjourney DMs.
2.  **Web Dashboard Workflow:** Open the image in the web interface, click **Image** to set it as a reference, or copy the direct URL straight from the creation card menu.

Aspect ratios impact how `--cref` reads character proportions. If your anchor image is square and your destination prompt uses a widescreen aspect ratio, Midjourney may stretch or compress physical features to fit the new aspect ratio. Keeping your reference aspect ratio similar to your target output aspect ratio can help prevent face shape distortions.

For maximum identity stability across long production pipelines, generate a pose sheet showing three side-by-side angles of your character. Crop the face panels into individual reference links, or combine them into a single character sheet before running `--cref`.

---


<div class="ad-slot" data-ad-slot></div>

## Step 2: Controlling Wardrobe and Features with Character Weight (--cw)

Controlling the character weight parameter dictates how much original character data carries over to your target render.

Using a higher weight setting prompts Midjourney to copy the facial structure, hair style, and outfit from your `--cref` source image. In a multi-frame sequence of an action scene, setting a high character weight helps ensure your character's jacket and shirt stay consistent between cuts.

A lower weight setting isolates the facial features. Costume details, jacket textures, and hair props are dropped, allowing your text prompt to take more control over wardrobe.

```text
photo of an Asian woman with black hair, wearing a medieval leather armor plate, standing on a castle rampart --cref https://cdn.discordapp.com/attachments/1234/5678/anchor.png --cw [weight]
```

Mid-range weight values offer flexibility during dynamic environmental shots. If your character enters a scene with extreme warm sunset lighting or heavy rain, setting a moderate weight preserves facial geometry while allowing the atmosphere to re-color the hair and clothing naturally.

---

## Step 3: Combining Character Reference (--cref) with Style Reference (--sref)

Combining character references (`--cref`) with style references (`--sref`) lets you maintain identity while forcing specific visual aesthetics.

| Parameter / Technique | Exact Syntax | What It Locks | Best Used For |
| --- | --- | --- | --- |
| **Character Reference** | `--cref [URL]` | Facial features, identity, hair, costume | Maintaining continuous character identity |
| **Character Weight** | `--cw [weight]` | Extent of wardrobe and hair retention | Swapping outfits (lower weight) vs full lock (higher weight) |
| **Style Reference** | `--sref [URL]` | Color palette, lighting, medium, artistic texture | Applying distinct art styles to any scene |
| **Combined Reference** | `--cref [URL] --sref [URL] --cw [value]` | Character identity + art style | Rendering a consistent character inside a target graphic style |

To combine parameters without style bleeding into skin tones or facial structures, place the prompt text first, followed by `--cref`, `--sref`, and `--cw`:

```text
photo of an Asian woman with black hair, sitting in a neon diner --cref https://cdn.discordapp.com/attachments/1234/5678/anchor.png --sref https://cdn.discordapp.com/attachments/1234/9999/style.png --cw [weight]
```

If you notice style bleeding—where the artistic style reference distorts the character's facial anatomy—lower your `--cw` value or turn on Niji mode for anime-style assets.

---

## Advanced Production Techniques: How to Generate Consistent Characters in Midjourney v6 Across Angles and Frames

Maintaining character lock across dynamic video storyboards requires precise camera and angle prompts. Do not rely solely on `--cref` to turn a face; guide the generator using explicit cinematography terms.

Use camera direction modifiers directly in your prompt text:
*   `low angle shot, looking up at...`
*   `side profile view, looking left...`
*   `over-the-shoulder shot targeting...`
*   `dramatic key light, strong shadows...`

You can pass multiple image links into a single `--cref` command to average facial features across multiple reference renders:

```text
--cref https://cdn.site.com/front.png https://cdn.site.com/profile.png
```

Combining multiple angle references improves multi-angle rendering accuracy and reduces single-image bias.

To simplify repetitive generation prompts in Discord, use the `/prefer option set` command to build a shortcut:

1. Type `/prefer option set`.
2. Set the option name to your character's name (for example: `hero`).
3. Set the value to `--cref [URL] --cw [weight]`.

Now, typing `--hero` at the end of any prompt automatically appends your reference link and weight values.

For multi-character frames, `--cref` can cause identity bleeding where features merge across figures. To avoid this, render multi-character shots using base descriptions first, then isolate each character frame using targeted inpainting tools.

---

## Troubleshooting Character Distortions and Inpainting Fixes

Character referencing is a statistical feature match, not a 3D model engine. You will encounter glitches during high-volume generation batches.

Here is how to correct common failure points:

*   **Lingering Outfits Under Low Character Weight:** If original clothing colors bleed through when a low character weight is set, explicitly counter-prompt the old clothing item in your text prompt (e.g., add "wearing a red dress, no t-shirt").
*   **Distorted Eyes or Minor Asymmetry:** Use Midjourney's **Vary (Region)** feature. Highlight the affected eye or face region with the brush tool, leave the prompt intact, and re-render.
*   **Face Shape Distortion Across Aspect Ratios:** Avoid changing aspect ratios radically between your reference image and your target output. If your anchor is square, generate a new anchor in a widescreen aspect ratio before prompting cinematic shots.

If generative tools fail to resolve small defects, perform a manual touch-up in Photoshop, re-upload the cleaned PNG to Discord, and use the updated image URL as your new `--cref` master anchor.

---

## Continuous Production Workflows

Learning **how to generate consistent characters in midjourney v6** provides motion designers, animators, and storyframers with a reproducible image pipeline. By combining stable anchor URLs, precise character weights (`--cw`), and clean style reference links (`--sref`), you can significantly reduce or eliminate the need for manual repainting across multi-shot sequences.

Midjourney pricing plans scale based on fast GPU usage across these workflows:

*   **Basic Plan ($10/month or $8/month annually):** Includes 3.3 Fast GPU hours. Suitable for anchor image generation and lightweight testing.
*   **Standard Plan ($30/month or $24/month annually):** Includes 15 Fast GPU hours and unlimited Relax GPU mode.
*   **Pro Plan ($60/month or $48/month annually):** Includes 30 Fast GPU hours and unlimited Relax mode.
*   **Mega Plan ($120/month or $96/month annually):** Includes additional Fast GPU hours and unlimited Relax mode for high-volume studio pipelines.

Note that Fast GPU hours expire at the end of each billing cycle and do not roll over. Select a tier with unlimited Relax mode (Standard or higher) when iterating on high-volume character reference batches.

---

## Frequently asked questions

### What is the exact syntax difference between --cref and --sref in Midjourney v6?
`--cref` (Character Reference) targets facial identity, physical anatomy, and clothing details from a source image. `--sref` (Style Reference) ignores character identity and instead copies color palettes, medium textures, lighting conditions, and aesthetic artistic styles.

### How do I change a character's clothes while keeping their face identical?
Append a low `--cw` value at the end of your prompt alongside your `--cref` URL. Setting a low character weight drops wardrobe and hair reference data, locking primarily the facial identity while allowing your prompt text to define the new outfit.

### Can I use multiple reference image URLs in a single --cref parameter?
Yes. Space-separate multiple image URLs inside a single `--cref` parameter, like this: `--cref URL1 URL2`. Midjourney merges structural feature data across all provided links to build a unified character reference.

### Why is my character changing face shape when I change aspect ratios?
Midjourney scales reference features to fit the destination canvas dimensions. If your anchor image was generated as a square and your target render is set to a widescreen aspect ratio, facial proportions may shift or stretch. It is generally best to render your original master anchor image at the same aspect ratio you plan to use for your final sequence.

**Related:** [How to Design Modern Logos Using Ideogram AI: Full Guide](/ai-blog-factory/blog/design-modern-logos-using-ideogram-ai/)

**Related:** [4 Best AI Image Generators for Etsy Digital Products](/ai-blog-factory/blog/best-ai-image-generator-etsy-digital-products/)

**Related:** [Best AI Logo Generator for Custom Vector Graphics: Ranked](/ai-blog-factory/blog/best-ai-logo-generator-vector-graphics/)

**Related:** [Best AI Product Photography App for Shopify: 7 Tested](/ai-blog-factory/blog/best-ai-product-photography-app-shopify/)
