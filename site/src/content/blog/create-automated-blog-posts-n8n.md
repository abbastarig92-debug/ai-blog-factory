---
title: How to Create Automated Blog Posts with n8n (Free JSON)
slug: create-automated-blog-posts-n8n
description: Learn how to create automated blog posts with n8n using OpenAI and WordPress.
  Download the free JSON workflow blueprint to publish drafts instantly.
pubDate: '2026-11-20T14:08:03+00:00'
updatedDate: '2026-11-20T14:08:03+00:00'
author: ToolStack Lab Editorial
cluster: automation
format: how-to
keyword: how to create automated blog posts with n8n
tags:
- n8n
- automation
- wordpress
- ai blogging
- openai
cover: /covers/create-automated-blog-posts-n8n.svg
ogTitle: 'Automate Blog Posts with n8n: Free JSON Workflow Blueprint'
keyTakeaway: Building a hands-off publishing engine requires connecting triggers,
  AI models, and CMS endpoints with structured workflow logic.
faq:
- q: Can I use n8n to automate WordPress blog posts?
  a: Yes, n8n connects directly to the WordPress REST API, allowing you to generate
    AI content with OpenAI, create featured images with DALL-E, and publish fully
    formatted blog post drafts automatically.
- q: How do I import an n8n workflow blueprint?
  a: To import a blueprint, open your n8n canvas and press Ctrl + V (or Cmd + V) to
    paste the raw workflow JSON directly into your editor.
wordCount: 2119
affiliateLinks: []
sources:
- title: Automate blog content creation with GPT-4, Perplexity & WordPress | n8n workflow
    template
  url: https://n8n.io/workflows/3336-automate-blog-content-creation-with-gpt-4-perplexity-and-wordpress
- title: Built a fully controllable AI blog writing system in n8n. Here’s a breakdown
    of how it works. [Template provided!] - Built with n8n - n8n Community
  url: https://community.n8n.io/t/built-a-fully-controllable-ai-blog-writing-system-in-n8n-here-s-a-breakdown-of-how-it-works-template-provided/180724?tl=en
- title: 'Content farming - : AI-powered blog automation for WordPress | n8n workflow
    template'
  url: https://n8n.io/workflows/5230-content-farming-ai-powered-blog-automation-for-wordpress
- title: 'Build a Blog Research and Writer n8n Workflow: Complete Guide | Codecademy'
  url: https://www.codecademy.com/article/blog-research-writer-n8n-workflow
- title: Create an AI Agent to Automate your Blog Posts on n8n (Self-Learning)
  url: https://www.youtube.com/watch?v=c5vYE-ea9-Y
- title: How to Automate WordPress Blog Posts n8n AI Workflow (2026) - Carthage Electronics
  url: https://carthageelectronics.com/automate-wordpress-blog-posts-n8n-ai-2026
- title: Automate Your WordPress Blog in 2026 (AI + n8n)
  url: https://www.youtube.com/watch?v=AFFeP_bmYiU&vl=en-US
- title: Automate blog creation & publishing with Gemini, Ideogram AI and WordPress
    | n8n workflow template
  url: https://n8n.io/workflows/7941-automate-blog-creation-and-publishing-with-gemini-ideogram-ai-and-wordpress
draft: false
---

## Quickstart: The Complete n8n Automated Blogging Workflow (JSON Blueprint)

Building a hands-off content publishing engine requires connecting triggers, language models, image generators, and CMS endpoints without breaking formatting. If you want to learn how to create automated blog posts with n8n, this step-by-step guide walks through building a production-ready pipeline using n8n, OpenAI, and the WordPress REST API. You can import the workflow blueprint into your n8n instance and start publishing structured drafts within minutes.

```
[Trigger: RSS / Webhook / Database] 
              │
              ▼
  [OpenAI Node: Article Generation]
              │
              ▼
[OpenAI / DALL-E 3: Image Generation] ──► [HTTP Request: Upload Media to WP]
              │                                      │
              └───────────────┬──────────────────────┘
                              ▼
                 [n8n Wait / Approval Node]
                              │
                              ▼
            [WordPress Node: Publish Post Draft]
```

To import the workflow blueprint:
1. Open your n8n canvas and click the **+** menu or press `Ctrl + V` / `Cmd + V`.
2. Copy the JSON structure below and paste it directly onto your workflow canvas.
3. Replace the placeholder API credentials with your OpenAI key and WordPress application password.

```json
{
  "name": "Automated WordPress Blog Pipeline",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "blog-trigger",
        "options": {}
      },
      "name": "Webhook Trigger",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [250, 300]
    },
    {
      "parameters": {
        "model": "gpt-4o",
        "prompt": "=Write an SEO-optimized blog post based on this title: {{ $json.body.title }}. Include H2 and H3 subheadings in Markdown format.",
        "options": {}
      },
      "name": "OpenAI Generator",
      "type": "@n8n/n8n-nodes-langchain.openAi",
      "typeVersion": 1,
      "position": [470, 300]
    },
    {
      "parameters": {
        "resource": "image",
        "prompt": "=A clean, modern technical illustration representing: {{ $json.body.title }}"
      },
      "name": "DALL-E 3 Image Node",
      "type": "n8n-nodes-base.openAi",
      "typeVersion": 1,
      "position": [690, 300]
    },
    {
      "parameters": {
        "url": "https://your-wordpress-site.com/wp-json/wp/v2/media",
        "sendBinaryData": true,
        "binaryPropertyName": "data",
        "options": {}
      },
      "name": "Upload Media to WordPress",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.1,
      "position": [910, 300]
    },
    {
      "parameters": {
        "title": "={{ $('Webhook Trigger').item.json.body.title }}",
        "content": "={{ $('OpenAI Generator').item.json.text }}",
        "status": "draft",
        "additionalFields": {
          "featuredMedia": "={{ $json.id }}"
        }
      },
      "name": "WordPress Post Node",
      "type": "n8n-nodes-base.wordpress",
      "typeVersion": 1,
      "position": [1130, 300]
    }
  ],
  "connections": {
    "Webhook Trigger": { "main": [[{ "node": "OpenAI Generator", "type": "main", "index": 0 }]] },
    "OpenAI Generator": { "main": [[{ "node": "DALL-E 3 Image Node", "type": "main", "index": 0 }]] },
    "DALL-E 3 Image Node": { "main": [[{ "node": "Upload Media to WordPress", "type": "main", "index": 0 }]] },
    "Upload Media to WordPress": { "main": [[{ "node": "WordPress Post Node", "type": "main", "index": 0 }]] }
  }
}
```

---

## Prerequisites and Tool Setup

Before running the workflow, you must configure host permissions, API access keys, and authentication headers across your software stack.

### Self-Hosted n8n vs. n8n Cloud

The n8n Community Edition is free to self-host under its fair-code license, offering unlimited execution runs. Host it on platforms like InstaPods ($3 to $7 per month) or PikaPods (around $3.80 per month) to run production pipelines at low overhead costs. 

In contrast, n8n Cloud plans meter your usage by workflow execution limits (such as Business at €667 per month when billed annually). If your workflow executes hundreds of multi-step runs per week, self-hosting avoids per-execution overage charges.

| Platform | Execution Cost at Scale | Data Privacy / Self-Hosting | Complex Logic Handling | Best For |
| :--- | :--- | :--- | :--- | :--- |
| **n8n (Self-Hosted)** | Zero license fees; pay standard server costs ($3–$7/mo on Managed Pods or VPS) | Full control; data stays on your isolated instance | Advanced branch routing, JS/Python code nodes, and custom nodes | Teams wanting execution scale and custom security |
| **n8n (Cloud)** | Metered by execution volume (including Business at €667/mo) | Cloud-hosted; managed infrastructure | Native node support with pre-configured UI triggers | Developers wanting zero server maintenance |
| **Zapier / Make** | Pay per step/operation; costs escalate quickly at scale | SaaS only; data stored on vendor servers | Limited multi-branch workflows on lower tiers | Non-technical creators making simple connections |

### API Credentials Configuration

1. **OpenAI API**: Sign in to the OpenAI Platform dashboard, navigate to API Keys, and generate a new secret key. Model pricing varies significantly based on selection:
   - **GPT-4o**: $2.50 per 1M input tokens / $10 per 1M output tokens.
   - **GPT-4o-Mini**: $0.15 per 1M input tokens / $0.60 per 1M output tokens.
   - **DALL-E 3**: Priced per image generated.
2. **WordPress Application Passwords**: Log into your WordPress administrative dashboard. Navigate to **Users -> Profile**, scroll to **Application Passwords**, enter a name (e.g., `n8n-automation`), and click **Add New Application Password**. Copy the generated token immediately.

---


<div class="ad-slot" data-ad-slot></div>

## Step 1: Configuring the Trigger Node (RSS, YouTube, or Database)

Your automation pipeline requires a structured data trigger to launch executions reliably.

```
                  ┌────────────────────────┐
                  │    Trigger Ingress     │
                  └───────────┬────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ Webhook / Form  │  │   RSS Feed      │  │ Database / API  │
│ (Custom Topic)  │  │ (Industry News) │  │ (Airtable/Mongo)│
└────────┬────────┘  └────────┬────────┘  └────────┬────────┘
         │                    │                    │
         └────────────────────┼────────────────────┘
                              │
                              ▼
                  ┌────────────────────────┐
                  │ Deduplication Filter   │
                  └────────────────────────┘
```

You can trigger the pipeline using three main sources:
* **RSS Feeds**: Monitor industry publications for breaking news ideas.
* **Webhooks / Forms**: Pass incoming topic payloads directly from a custom form interface.
* **Database Nodes**: Pull scheduled content records from Airtable or MongoDB Atlas.

When extracting raw data from incoming payloads, extract the primary topic title, target keywords, and brief reference notes.

To prevent duplicate runs when monitoring RSS feeds, place an n8n **Filter** node directly after the trigger node. Store executed article titles or source URLs in a light database table (such as MongoDB or a simple JSON file). Configure the node to drop any execution where the payload URL already matches a previously logged record.

---

## How to Create Automated Blog Posts with n8n: Structuring AI Generation and Markdown Parsing

Generating long-form content directly in a single prompt often produces unstructured text walls. Instead, chain multi-step language model nodes to separate structural outlining, body drafting, and SEO optimization.

```
┌────────────────────┐     ┌────────────────────┐     ┌────────────────────┐
│ Step 2A: Outline   │ ──► │ Step 2B: Full Draft│ ──► │ Step 2C: Markdown  │
│ Structure (GPT-4o) │     │ Content (GPT-4o)   │     │ HTML Conversion    │
└────────────────────┘     └────────────────────┘     └────────────────────┘
```

### System Prompts for Voice Control

To maintain brand consistency and avoid generic AI phrasing, use strict system instructions inside your OpenAI node:

```text
You are a senior technical writer. Write an in-depth article using the provided context.
Rules:
1. Format output using clean Markdown syntax (H2, H3, bold emphasis, ordered/unordered lists).
2. Avoid generic filler language like "In today's fast-paced world" or "game-changer".
3. Use a direct, practical, first-person narrative tone.
4. Keep paragraphs short (1 to 3 sentences maximum).
```

### Converting Markdown to Semantic HTML

WordPress accepts both raw text and HTML structures. While standard Markdown text renders inside Gutenberg blocks, parsing content to semantic HTML inside n8n ensures custom styling and tag formatting remain intact.

Use an n8n **Code** node (JavaScript) running a standard parsing script to convert the generated Markdown into clean HTML output before sending it downstream:

```javascript
// Convert basic Markdown headers and inline styles into HTML strings
let markdownText = $input.first().json.text;

let htmlText = markdownText
  .replace(/^### (.*$)/gim, '<h3>$1</h3>')
  .replace(/^## (.*$)/gim, '<h2>$1</h2>')
  .replace(/^# (.*$)/gim, '<h1>$1</h1>')
  .replace(/\*\*(.* vastness rhetoric sentence .*?)\*\*/gim, '<strong>$1</strong>')
  .replace(/\*(.* vastness rhetoric sentence .*?)\*/gim, '<em>$1</em>')
  .replace(/\n\n/g, '</p><p>');

return [{ json: { htmlContent: `<p>${htmlText}</p>` } }];
```

---

## Step 3: Automated Featured Image Generation and Media Uploads

A post published without visual assets suffers lower engagement. Automatically generate contextually relevant imagery and attach it directly through the WordPress REST API.

```
┌────────────────────┐     ┌────────────────────┐     ┌────────────────────┐
│ Create Contextual  │ ──► │ Fetch Image Data   │ ──► │ HTTP POST Upload to│
│ Prompt (DALL-E 3)  │     │ (Binary Stream)    │     │ /wp-json/wp/v2/media│
└────────────────────┘     └────────────────────┘     └─────────┬──────────┘
                                                                │
                                                                ▼
                                                      [Capture Attachment ID]
```

### 1. Generating Images with DALL-E 3
Add an OpenAI node configured to call DALL-E 3. Pass the generated article title to construct a visual prompt:
`"A professional, minimalist header graphic illustrating [Topic Title], digital vector style, 16:9 aspect ratio."`

### 2. Fetching Image Data and Uploading to WordPress
The DALL-E 3 node returns a temporary URL. Add an **HTTP Request** node to fetch the raw image binary data:
* **Method**: GET
* **URL**: `={{ $json.url }}`
* **Response Format**: File / Binary Data

Next, pipe that binary data into a second **HTTP Request** node targeting the WordPress Media endpoint:
* **Method**: POST
* **URL**: `https://your-domain.com/wp-json/wp/v2/media`
* **Authentication**: Header Auth or Basic Auth (using your WordPress username and Application Password).
* **Headers**: 
  * `Content-Disposition`: `attachment; filename="featured-image.png"`
  * `Content-Type`: `image/png`
* **Send Binary Data**: Enabled (Property Name: `data`).

The API response returns a JSON object containing the uploaded file details. Extract the `id` key, which represents the unique WordPress **Attachment ID**.

---

## Step 4: Publishing to WordPress via REST API

With your HTML content and featured media attachment ID generated, pass the payload to the WordPress node.

```
┌────────────────────────────────────────────────────────┐
│               n8n WordPress Post Node                  │
├────────────────────────────────────────────────────────┤
│ Title:    {{ $node["Trigger"].json["title"] }}         │
│ Content:  {{ $node["Code Node"].json["htmlContent"] }} │
│ Status:   draft                                        │
│ Featured: {{ $node["Upload Media"].json["id"] }}       │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
               ┌────────────────────────┐
               │ WordPress REST API     │
               │ (/wp-json/wp/v2/posts)  │
               └────────────────────────┘
```

### Node Field Mappings
Select the native **WordPress Node** (or an **HTTP Request Node** pointing to `/wp-json/wp/v2/posts`) and set the following parameter mappings:

* **Title**: `={{ $('Trigger').item.json.title }}`
* **Content**: `={{ $('Code Node').item.json.htmlContent }}`
* **Status**: Set to `draft` (recommended for safety) or `publish`.
* **Featured Media**: `={{ $('Upload Media').item.json.id }}`
* **Slug**: `={{ $('Trigger').item.json.title.toLowerCase().replace(/[^a-z0-9]+/g, '-') }}`

### Handling Network Faults and Retries
REST API requests can fail due to web application firewall blocks or server timeouts. Open the node's **Settings** tab in n8n and toggle:
* **Retry On Fail**: Enabled
* **Max Tries**: Set to your desired number of retry attempts
* **Wait Between Tries**: Set a brief delay between attempts

---

## Step 5: Implementing Human-in-the-Loop Quality Safeguards

Publishing fully unedited AI content directly to a production blog risks formatting glitches or unverified facts. Inserting a human review step prevents faulty posts from reaching live readers.

```
┌────────────────────┐     ┌────────────────────┐     ┌────────────────────┐
│ AI Generation &    │ ──► │ n8n Wait Node      │ ──► │ Slack Notification │
│ Media Processing   │     │ (Webhook Callback) │     │ (Approval Button)  │
└────────────────────┘     └────────────────────┘     └─────────┬──────────┘
                                                                │
                                            ┌───────────────────┴───────────────────┐
                                            ▼                                       ▼
                                   [ Click: Approve ]                      [ Click: Reject ]
                                            │                                       │
                                            ▼                                       ▼
                                 [ Publish to WordPress ]                [ Halt Execution / Log ]
```

1. Add a **Wait** node after content parsing. Set the trigger condition to wait for an incoming **Webhook Call**.
2. Configure a **Slack** (or Telegram) node to send a notification message containing the post draft preview along with two action buttons:
   * **Approve Link**: `https://n8n.yourdomain.com/webhook/approve?executionId={{ $execution.id }}`
   * **Reject Link**: `https://n8n.yourdomain.com/webhook/reject?executionId={{ $execution.id }}`
3. When you click **Approve** in Slack, the Wait node resolves and releases the execution flow down the path to update the post status from `draft` to `publish`.

---

## Frequently Asked Questions

### Can I self-host n8n to generate automated blog posts for free?
Yes. The n8n Community Edition license is free to self-host without software execution limits. You will only pay for your underlying hosting server infrastructure (such as InstaPods at $3–$7 per month or raw VPS servers) and third-party API usage (such as OpenAI token costs).

### How do I attach a generated image to a WordPress post automatically in n8n?
Fetch the binary image stream using an HTTP Request node and send a `POST` request to the WordPress `/wp-json/wp/v2/media` endpoint. Capture the returned `id` property from the JSON response and map it directly into the `featured_media` field inside your WordPress post creation node.

### How do I add a human review step before n8n publishes an AI blog post?
Place an n8n **Wait Node** set to resume on webhook reception right before the publishing step. Send an automated approval link to your Slack or email client containing the unique execution ID callback URL so you can approve or discard the draft with a single click.

### What is the best way to handle Markdown-to-HTML conversion in n8n?
The standard method uses a custom JavaScript **Code Node** running regular expression string replacements to convert headers, emphasis tags, and line breaks into standard semantic HTML elements (`<h2>`, `<p>`, `<strong>`). You can also pass the raw string through a lightweight JavaScript Markdown library inside the node.

---

## Final Workflow Checklist

Understanding how to create automated blog posts with n8n allows content teams to scale production without sacrificing quality control. By coupling self-hosted n8n instances with strict system prompts, image upload pipelines, and human approval checkpoints, you maintain full editorial authority over your publishing flow while reducing routine manual tasks.

**Related:** [How to Automate AI Blog Posts With n8n and Koala AI](/ai-blog-factory/blog/automate-ai-blog-posts-n8n-koala/)

**Related:** [How to Build Automated YouTube Workflow in n8n (Free)](/ai-blog-factory/blog/n8n-automated-youtube-workflow/)

**Related:** [Activepieces vs n8n for Small Business Automation Compared](/ai-blog-factory/blog/activepieces-vs-n8n-small-business-automation/)

**Related:** [Auto Post Instagram Reels with n8n Workflow (Free JSON)](/ai-blog-factory/blog/auto-post-instagram-reels-n8n-workflow/)
