---
title: Auto Post Instagram Reels with n8n Workflow (Free JSON)
slug: auto-post-instagram-reels-n8n-workflow
description: Stop paying for social media tools. Learn how to auto post instagram
  reels with n8n workflow using our free JSON blueprint and Meta API polling logic.
pubDate: '2026-09-18T09:39:14+00:00'
updatedDate: '2026-09-18T09:39:14+00:00'
author: ToolStack Lab Editorial
cluster: automation
format: how-to
keyword: how to auto post instagram reels with n8n workflow
tags:
- n8n
- instagram automation
- meta api
- workflow automation
- low-code
cover: /covers/auto-post-instagram-reels-n8n-workflow.svg
ogTitle: 'Automate Instagram Reels for Free: n8n Workflow & Meta API Guide'
keyTakeaway: Eliminate monthly subscription costs by building a custom, self-hosted
  Instagram automation engine using n8n and native Meta API polling logic.
faq:
- q: Why use n8n for Instagram Reels automation?
  a: n8n allows you to bypass expensive third-party subscription tools by connecting
    directly to the Meta API, giving you full control over your automation logic and
    data privacy.
- q: How does this workflow handle Meta API timeouts?
  a: The workflow includes a self-contained polling loop that monitors the video container
    status, ensuring the Reel is only published once Meta's servers have fully processed
    the file.
wordCount: 1876
affiliateLinks: []
sources:
- title: Auto-generate and post Instagram reels with Veo3, OpenAI, and Blotato | n8n
    workflow template
  url: https://n8n.io/workflows/5910-auto-generate-and-post-instagram-reels-with-veo3-openai-and-blotato
- title: How to Automate Instagram Reels With AI (24/7 Posting System) - Blotato
  url: https://www.blotato.com/blog/automate-instagram-reels
- title: 'n8n Instagram Upload: Reels & Posts with HTTP Request | Upload-Post.com'
  url: https://www.upload-post.com/n8n/instagram-reels-upload
- title: How To Post To Instagram Via N8N [AI Automation]
  url: https://www.youtube.com/watch?v=PXcDqmamX2Q
- title: N8N Instagram Automation | Step-by-Step Guide (Free Template)
  url: https://www.youtube.com/watch?v=m02TeQ9kHVo&vl=en
- title: 'Full Social Media Automation: AI Images (Runware) + Trending Topics (Perplexity)
    → Instagram, Facebook, LinkedIn + Auto-Comments - Built with n8n - n8n Community'
  url: https://community.n8n.io/t/full-social-media-automation-ai-images-runware-trending-topics-perplexity-instagram-facebook-linkedin-auto-comments/249592?tl=en
- title: 'Full Social Media Automation: AI Images (Runware) + Trending Topics (Perplexity)
    → Instagram, Facebook, LinkedIn + Auto-Comments - Built with n8n - n8n Community'
  url: https://community.n8n.io/t/full-social-media-automation-ai-images-runware-trending-topics-perplexity-instagram-facebook-linkedin-auto-comments/249592?tl=
- title: Automated Instagram reels workflow | n8n workflow template
  url: https://n8n.io/workflows/5139-automated-instagram-reels-workflow
draft: false
---

If you publish short-form video, you know Meta's official API is notoriously finicky. This step-by-step guide walks you through exactly **how to auto post instagram reels with n8n workflow** without paying for expensive third-party wrappers or middleware tools. We will bypass the typical timeouts by building an automated, self-contained polling loop that waits for Meta's servers to process your video container.

## Complete n8n Instagram Reels Auto-Post Workflow (JSON Download & Architecture)

This production-ready JSON blueprint handles video sourcing, container creation, asynchronous status polling, and publication. Paste this code directly into your n8n canvas to get started.

```json
{
  "name": "Instagram Reels Auto-Poster",
  "nodes": [
    {
      "parameters": {
        "rule": {
          "interval": [
            {
              "field": "hours",
              "hoursInterval": 6
            }
          ]
        }
      },
      "id": "a90dfbd8-1234-4567-89ab-cdef12345678",
      "name": "Schedule Trigger",
      "type": "n8n-nodes-base.scheduleTrigger",
      "typeVersion": 1.1,
      "position": [100, 300]
    },
    {
      "parameters": {
        "method": "POST",
        "url": "=https://graph.facebook.com/v19.0/{{$json.ig_user_id}}/media",
        "sendBody": true,
        "specifyBody": "json",
        "jsonBody": "={\n  \"media_type\": \"REELS\",\n  \"video_url\": \"{{$json.video_direct_url}}\",\n  \"caption\": \"{{$json.caption}}\",\n  \"access_token\": \"{{$json.access_token}}\"\n}",
        "options": {}
      },
      "id": "b11efbd8-1234-4567-89ab-cdef12345679",
      "name": "Create IG Container",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.1,
      "position": [300, 300]
    },
    {
      "parameters": {
        "amount": 20,
        "unit": "seconds"
      },
      "id": "c22efbd8-1234-4567-89ab-cdef12345680",
      "name": "Wait 20s",
      "type": "n8n-nodes-base.wait",
      "typeVersion": 1,
      "position": [500, 300]
    },
    {
      "parameters": {
        "method": "GET",
        "url": "=https://graph.facebook.com/v19.0/{{$json.id}}",
        "sendQuery": true,
        "queryParameters": {
          "parameters": [
            {
              "name": "fields",
              "value": "status_code"
            },
            {
              "name": "access_token",
              "value": "={{$node[\"Create IG Container\"].json.access_token}}"
            }
          ]
        },
        "options": {}
      },
      "id": "d33efbd8-1234-4567-89ab-cdef12345681",
      "name": "Check Container Status",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.1,
      "position": [700, 300]
    },
    {
      "parameters": {
        "conditions": {
          "string": [
            {
              "value1": "={{$json.status_code}}",
              "value2": "FINISHED"
            }
          ]
        }
      },
      "id": "e44efbd8-1234-4567-89ab-cdef12345682",
      "name": "Is Video Ready?",
      "type": "n8n-nodes-base.if",
      "typeVersion": 1,
      "position": [900, 300]
    },
    {
      "parameters": {
        "method": "POST",
        "url": "=https://graph.facebook.com/v19.0/{{$node[\"Create IG Container\"].json.ig_user_id}}/media_publish",
        "sendBody": true,
        "specifyBody": "json",
        "jsonBody": "={\n  \"creation_id\": \"{{$node[\"Create IG Container\"].json.id}}\",\n  \"access_token\": \"{{$node[\"Create IG Container\"].json.access_token}}\"\n}",
        "options": {}
      },
      "id": "f55efbd8-1234-4567-89ab-cdef12345683",
      "name": "Publish Reel",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.1,
      "position": [1100, 200]
    }
  ],
  "connections": {
    "Schedule Trigger": {
      "main": [
        [
          {
            "node": "Create IG Container",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Create IG Container": {
      "main": [
        [
          {
            "node": "Wait 20s",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Wait 20s": {
      "main": [
        [
          {
            "node": "Check Container Status",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Check Container Status": {
      "main": [
        [
          {
            "node": "Is Video Ready?",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Is Video Ready?": {
      "main": [
        [
          {
            "node": "Publish Reel",
            "type": "main",
            "index": 0
          }
        ],
        [
          {
            "node": "Wait 20s",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  }
}
```

The high-level architecture flows through four clear phases:

```
[Storage Trigger] ──> [Meta Container Creation] ──> [Polling Loop] ──> [Media Publish]
 (Fetch MP4 URL)       (POST /media -> Get ID)      (Check status)     (POST /media_publish)
```

We configure the schedule trigger to run on a regular schedule. This creates a safety buffer that helps prevent Meta API rate limiting. 

Running executions too close together can trigger spam filters on your Meta developer account. Spacing posts out sufficiently keeps your publishing pipeline clean.

---

## Prerequisites & Meta Graph API App Configuration

Before configuring n8n, you must set up your Meta developer credentials. Meta strictly restricts access to its Graph API.

### Step 1: Link Instagram to Facebook
Convert your Instagram account to a Professional or Business Account in the Instagram mobile app settings. Next, create a public Facebook Page and link your Instagram Business Account to it in your Facebook Page settings.

### Step 2: Create a Meta Developer App
Go to the Meta for Developers portal and click **Create App**. Select **Other** as your use case, then choose **Business** as the app type.

Add the **Instagram Graph API** product to your app. Copy your **Instagram Business Account ID** from the Meta App Dashboard under the API settings.

### Step 3: Generate a Long-Lived Access Token
Short-lived user tokens expire quickly. To get a long-lived token, open the Meta Graph API Explorer, select your App, and choose these scopes:

*   `instagram_basic`
*   `instagram_content_publish`
*   `pages_read_engagement`
*   `pages_show_list`

Generate the short-lived token, then make a `GET` call to the exchange endpoint:

```http
GET https://graph.facebook.com/v19.0/oauth/access_token
  ?grant_type=fb_exchange_token
  &client_id={your-app-id}
  &client_secret={your-app-secret}
  &fb_exchange_token={short-lived-token}
```

This returns a long-lived token. To keep your workflow running, set up a secondary n8n workflow that calls this endpoint periodically to refresh the token automatically.

---


<div class="ad-slot" data-ad-slot></div>

## Configuring the n8n Nodes: Step-by-Step Setup

With credentials in hand, we can build the individual n8n processing nodes.

### Node 1: Sourcing the Video URL
Meta requires a direct, publicly accessible download link to your video file. If you use Google Drive, you must parse the file ID and format it as a direct download link.

```
https://drive.google.com/uc?export=download&id={FILE_ID}
```

If you use AWS S3, generate a presigned URL with an appropriate expiration window. This gives Meta's ingest servers enough time to retrieve the file.

### Node 2: Create the Media Container
Add an **HTTP Request** node to your n8n workspace. Set the parameters exactly as shown here:

*   **Method**: `POST`
*   **URL**: `https://graph.facebook.com/v19.0/{{$json.ig_user_id}}/media`
*   **Body Content**: JSON
*   **Fields**:
    *   `media_type`: `REELS`
    *   `video_url`: `{{$json.video_direct_url}}`
    *   `caption`: `{{$json.caption}}`
    *   `access_token`: `{{$json.access_token}}`

This node returns a JSON payload containing an ID. This is your temporary container ID:

```json
{
  "id": "18023948572910293"
}
```

Extract this ID using the expression `{{$json.id}}` to pass it to the verification loop.

---

## Resolving Processing Delays: How to Auto Post Instagram Reels with n8n Workflow Polling Loop

When you send a video to Meta, their servers must transcode, compress, and render the file. This process is asynchronous. 

If you immediately try to publish using the container ID, the API will fail with a `Media container is not ready` error. You must build a polling loop to query the container status before executing the final publish step.

```
                  ┌────────────────────────┐
                  │   Create Container     │
                  └───────────┬────────────┘
                              │
                              ▼
                      [ Wait Interval ]
                              │
                              ▼
                  ┌────────────────────────┐
                  │ Check Container Status │
                  └───────────┬────────────┘
                              │
                              ▼
                      /               \
                     /  Is Status      \
                    <   "FINISHED"?     >
                     \                 /
                      \               /
                        /          \
                      YES          NO
                      /              \
                     ▼                ▼
             ┌──────────────┐   [ Wait Interval ]
             │ Publish Reel │         │
             └──────────────┘         └─ (Loop back to Check)
```

To build this in n8n:

1.  Connect a **Wait** node directly to your **Create IG Container** node. Set the delay duration to an appropriate interval.
2.  Add another **HTTP Request** node named **Check Container Status**. Set the method to `GET` and point it to:
    `https://graph.facebook.com/v19.0/{{$node["Create IG Container"].json.id}}`
3.  Add query parameters for `fields` (value: `status_code`) and `access_token`.
4.  Create an **If** node. Set the condition to check if `{{$json.status_code}}` equals `FINISHED`.
5.  Connect the **False** output of the If node back to the input of the **Wait** node. 
6.  Connect the **True** output to your final publishing node.

This loop checks the status periodically. If the status is `IN_PROGRESS`, it waits and checks again. If it returns `FINISHED`, the workflow proceeds to publish.

---

## Publishing the Reel & Setting Up Error Notifications

Once the container status is verified as `FINISHED`, execute the final publishing call.

### Node 3: Publish the Reel
Add a final **HTTP Request** node to your workflow:

*   **Method**: `POST`
*   **URL**: `https://graph.facebook.com/v19.0/{{$node["Create IG Container"].json.ig_user_id}}/media_publish`
*   **Body Parameters**:
    *   `creation_id`: `{{$node["Create IG Container"].json.id}}`
    *   `access_token`: `{{$json.access_token}}`

### Handling Failures
Automations eventually hit API limits or network issues. Connect an **Error Trigger** node to your canvas. Route its output to a Slack or Discord webhook node. 

Tracking the exact API response payload in Discord alerts simplifies troubleshooting. Configure the alert payload to output the exact error message from Meta:

```json
{
  "error": "={{$json.execution.error.message}}",
  "node": "={{$json.execution.nodeName}}"
}
```

This alert immediately tells you if a post failed due to an expired token, a missing S3 file, or an invalid video aspect ratio.

---

## Video Formatting Specifications & Caption Engineering

Meta's ingestion servers reject videos that do not meet their formatting guidelines. Ensure your video rendering pipeline outputs files that comply with Meta's requirements for aspect ratio, codecs, file size, and duration.

You can use an n8n **Code** node to format your captions before sending them to Meta. This node cleans up system strings, inserts line breaks, and appends your target hashtags dynamically.

```javascript
// n8n Code Node (JavaScript)
const captionText = $input.item.json.raw_caption;
const dynamicHashtags = "#automation #n8n #nocode";

// Replace literal newlines with encoded characters Meta accepts
const formattedCaption = captionText.replace(/\n/g, '\n') + '\n\n' + dynamicHashtags;

return {
  caption: formattedCaption
};
```

To set a custom cover image, add the optional `cover_url` parameter to your initial **Create IG Container** HTTP request. Provide a direct URL to a JPG or PNG file matching your video's vertical aspect ratio.

---

## Comparison of Automation Methods

Choosing the right tool for auto-posting depends on your execution volume and technical resources.

| Feature / Metric | n8n Custom Workflow | Zapier / Make.com | Native Buffer / Hootsuite |
| :--- | :--- | :--- | :--- |
| **Cost** | Free (Self-hosted) or €20/mo (Cloud Starter) | Varies (escalates with volume) | Varies (limited by channels) |
| **Execution Limits** | Unlimited (Self-hosted) or 2,500/mo (Cloud) | Strict monthly task caps | Strictly limited scheduled posts |
| **Custom Code Blocks** | Native JS/Python nodes | Highly restricted | None |
| **Custom Polling Loops**| Fully customizable loops | Difficult or requires paid add-ons | Not supported |
| **Setup Complexity** | Medium (Requires Meta App Setup) | Low | Low |

---

## Frequently asked questions

### Why does my Instagram Reel post fail with 'Media container is not ready' and how do I fix it in n8n?
Meta processes uploaded video files asynchronously. If you try to publish immediately after creating the container, the file is still rendering on Meta's servers. To fix this, build a loop in n8n that queries the container ID status endpoint periodically and only triggers the publish node when the status returns `FINISHED`.

### How do I extract a direct, publicly accessible MP4 link from Google Drive or S3 for n8n?
For Google Drive, change the share settings of the file to "Anyone with the link can view," then extract the file ID and format your URL as `https://drive.google.com/uc?export=download&id={FILE_ID}`. For AWS S3, generate a presigned URL using an S3 node with an appropriate expiration window to allow Meta's servers to download the video.

### How do I generate a long-lived access token for Instagram Graph API that doesn't expire quickly?
Generate a short-lived token in the Meta Graph API Explorer, then use the `/oauth/access_token` endpoint along with your Meta App ID and App Secret to exchange it for a long-lived token. To maintain access, build a simple recurring n8n workflow that refreshes this token periodically.

### What are the exact API endpoints and payload structures required to post an Instagram Reel programmatically?
First, send a `POST` request to `graph.facebook.com/v19.0/{ig-user-id}/media` containing `media_type=REELS`, `video_url`, and `caption`. Once the container is processed, send a `POST` request to `graph.facebook.com/v19.0/{ig-user-id}/media_publish` containing the returned `creation_id`.

---

## Conclusion

By routing your video assets through a custom polling loop, you can bypass the common errors that plague typical social media automations. Understanding **how to auto post instagram reels with n8n workflow** gives you complete control over your publishing pipeline. You avoid expensive third-party SaaS tools, bypass rigid schedule limits, and maintain absolute ownership of your content distribution engine.

**Related:** [How to Build Automated YouTube Workflow in n8n (Free)](/ai-blog-factory/blog/n8n-automated-youtube-workflow/)

**Related:** [Best n8n Nodes for Scraping Website Content Automatically](/ai-blog-factory/blog/best-n8n-nodes-for-scraping-content/)

**Related:** [Best n8n Workflow Templates for Content Marketing Teams](/ai-blog-factory/blog/best-n8n-workflow-templates-content-marketing/)

**Related:** [Make.com vs n8n for Content Creators: Save Time & Money](/ai-blog-factory/blog/make-com-vs-n8n-content-creators/)
