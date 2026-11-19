---
title: How to Auto Post YouTube Shorts with n8n Workflow
slug: auto-post-youtube-shorts-n8n-workflow
description: Stop manual uploads and save hours by learning how to auto post youtube
  shorts with n8n workflow using this production-ready resumable upload template.
pubDate: '2026-11-19T14:35:49+00:00'
updatedDate: '2026-11-19T14:35:49+00:00'
author: ToolStack Lab Editorial
cluster: automation
format: how-to
keyword: how to auto post youtube shorts with n8n workflow
tags:
- n8n
- youtube automation
- workflow automation
- video marketing
- api
cover: /covers/auto-post-youtube-shorts-n8n-workflow.svg
ogTitle: 'Automate Your YouTube Shorts: The Ultimate n8n Workflow Guide'
keyTakeaway: Automating YouTube Shorts with n8n eliminates manual metadata mapping
  and ensures consistent posting through a reliable resumable upload pipeline.
faq:
- q: How does the n8n workflow handle large video files?
  a: The workflow utilizes a resumable upload strategy to ensure binary data transfers
    reliably to the YouTube Data API v3, preventing failures during high-volume posting.
wordCount: 1248
affiliateLinks: []
sources:
- title: Auto-post YouTube Shorts from Google Drive with OpenRouter AI titles & descriptions
    | n8n workflow template
  url: https://n8n.io/workflows/11441-auto-post-youtube-shorts-from-google-drive-with-openrouter-ai-titles-and-descriptions
- title: 🎬 YouTube shorts automation tool 🚀 | n8n workflow template
  url: https://n8n.io/workflows/2941-youtube-shorts-automation-tool
- title: I Built a YouTube Shorts Automation with n8n… It Posts VIRAL Shorts Every
    30 Mins!
  url: https://www.youtube.com/watch?v=kBS1MiDr4LY
- title: Automatic YouTube shorts generator | n8n workflow template
  url: https://n8n.io/workflows/2856-automatic-youtube-shorts-generator
- title: 'Full Social Media Automation: AI Images (Runware) + Trending Topics (Perplexity)
    → Instagram, Facebook, LinkedIn + Auto-Comments - Built with n8n - n8n Community'
  url: https://community.n8n.io/t/full-social-media-automation-ai-images-runware-trending-topics-perplexity-instagram-facebook-linkedin-auto-comments/249592?tl=en
- title: Fully automated AI video generation & multi-platform publishing | n8n workflow
    template
  url: https://n8n.io/workflows/3442-fully-automated-ai-video-generation-and-multi-platform-publishing
- title: Generate & auto-post social videos to multiple platforms with GPT-4 and Kling
    AI | n8n workflow template
  url: https://n8n.io/workflows/3501-generate-and-auto-post-social-videos-to-multiple-platforms-with-gpt-4-and-kling-ai
- title: 'Claude Anthropic AI ● Prompts, Code, Agents, Automation, Tips, MCP, Tools
    | Social Media Automation: Publish One Video to 9 Platforms Automatically  | Facebook'
  url: https://www.facebook.com/groups/aibusinesstools/posts/1800642478008342
draft: false
---

Finding a stable configuration for high-volume posting can be challenging when dealing with API limits. This guide details **how to auto post youtube shorts with n8n workflow** to help streamline the upload process. Using a resumable upload strategy can help ensure your vertical videos are transferred reliably. By following this technical setup, you can move toward an automated pipeline that handles metadata mapping and file binary transfers.

## Quick Setup: Using an n8n YouTube Shorts Workflow Template

Using a production-ready JSON template can handle the management of binary data and API authentication.

**[Access the n8n YouTube Shorts JSON Template]**

The workflow follows a linear logic:
1.  **Trigger**: Polls a Google Drive folder periodically for new files.
2.  **Filter**: Checks if the file extension is a supported video format like .mp4 or .mov.
3.  **Fetch**: Downloads the binary data into the n8n execution environment.
4.  **Metadata**: Extracts the filename to create a title and appends relevant tags.
5.  **Upload**: Sends the file to YouTube via the Data API v3.
6.  **Cleanup**: Moves the file to a processed folder so it isn't handled twice.

To get started, open your n8n instance, click "Import from File," and select the JSON. You will likely need to connect your credentials for the Google Drive and YouTube nodes.

## Prerequisites: Configuring the YouTube Data API v3

The YouTube node in n8n requires OAuth2 credentials. Follow these steps in the Google Cloud Console to get authorized.

**Create a Project and Enable APIs**
Go to the Google Cloud Console and create a new project. Navigate to the "Enabled APIs & Services" tab and search for **YouTube Data API v3**. Click "Enable." This API operates on a quota system. According to current limits, projects typically get a default allocation of 10,000 units per day. Since a `videos.insert` call costs 1,600 units, a standard project can handle approximately six uploads per day unless you request a quota extension.

**Set Up OAuth2 Credentials**
1.  Go to **APIs & Services > OAuth consent screen**.
2.  Select "External" and fill in the required application details.
3.  Add your own email as a "Test User" to ensure the application remains accessible during testing.
4.  Go to **Credentials > Create Credentials > OAuth client ID**.
5.  Select "Web application."
6.  Add the Redirect URI provided by your n8n YouTube node.


<div class="ad-slot" data-ad-slot></div>

## Step 1: Setting Up the Trigger (Google Drive or Dropbox)

Monitoring a folder is often more efficient than a "Webhook" trigger for video, as it allows for bulk processing. In the Google Drive node, set the **Resource** to "File" and **Operation** to "List." 

**Filter for Video Files**
Use a "Filter" node immediately after the trigger to ensure only video files are processed. Set the filter to only allow files where the name contains appropriate video extensions like `.mp4`.

**Download the Binary Data**
The "List" operation provides file metadata. You must add a second Google Drive node with the operation **Download**, passing the `File ID` from the previous step. This loads the actual video bytes into n8n's memory. If you are self-hosting on a system with limited RAM, be cautious with very large files, as concurrent executions can impact performance.

## Step 2: Automating Metadata and the 'Shorts' Flag

YouTube typically categorizes a video as a Short if it is vertical (9:16 aspect ratio) and its duration is under 60 seconds.

**Formatting the Title and Description**
Use an **Edit Fields (Set)** node to prepare your metadata.
*   **Title**: Use an expression to clean up the filename for the title.
*   **Description**: Including `#Shorts` in the description can act as a signal for the Shorts shelf.

**Optional AI Enrichment**
To customize content, you can insert an AI node before the upload. Pass the filename to the AI and ask it to generate a relevant title and hashtags. This can transform a generic filename into a more descriptive title with relevant tags.

## Step 3: Configuring the YouTube Node for Automated Uploads

Connect the **YouTube Node** and set the **Resource** to "Video" and **Operation** to "Upload."

**Mapping Binary Properties**
In the "Video File" field, enter the name of the binary property from the Download node (usually `data`). If this is mapped incorrectly, the API may return an error.

**Setting the Privacy Status**
It is often helpful to set the **Privacy Status** to "Private" or "Unlisted" initially. This allows for a final check of the alignment and captions before the video is made public.

| Feature | n8n Workflow | Zapier/Make | Manual Upload |
| :--- | :--- | :--- | :--- |
| **Daily Upload Limit** | API restricted (approx. 6/day default) | Plan dependent | High |
| **File Size Limit** | Dependent on hosting | Plan dependent | High |
| **Cost** | Free options (Self-hosted) | Paid plans | Free |
| **Custom Logic** | High (Code nodes) | Limited | None |
| **Auto-Cleanup** | Yes (Moves files) | Limited | Manual |

## Advanced: Error Handling and Notifications

To prevent losing track of uploads, you can add an **Error Trigger** node to your canvas. 

Create a separate branch that triggers if the main workflow encounters an issue. Connect this to a notification node, such as **Slack** or **Discord**, configured to include the filename and the error message.

If you are uploading multiple files, adding a **Wait Node** between uploads can help maintain stability and avoid hitting rate-limiting flags.

## Troubleshooting Common API and Formatting Issues

**Solving Payload Size Limits**
If you are self-hosting n8n and encounter limits with large binary files, you may need to adjust environment variables such as `N8N_PAYLOAD_SIZE_MAX` to a value sufficient for your typical file sizes.

**Handling OAuth2 Token Expiration**
If the workflow stops working after a short period, check if your Google Cloud project is still in "Testing" mode. You may need to move the app to "Production" status or ensure your test users are correctly configured.

**The 60-Second Rule**
YouTube is strict regarding duration. A video exceeding 60 seconds will generally be treated as a standard video rather than a Short. You can use a "Code" node to check file metadata before uploading to ensure the duration meets the requirements.

## Frequently asked questions

### How do I make sure YouTube recognizes the video as a Short?
Ensure the video is rendered in a 9:16 aspect ratio and the duration is under 60 seconds. Adding `#Shorts` to the description or title can also assist with correct indexing.

### What are the file size limits when uploading through n8n?
Self-hosted versions of n8n can generally handle sizes allowed by your server's RAM and storage. Keeping files at a reasonable size helps the "Resumable Upload" function work reliably.

### Can I schedule the post for a specific time using this workflow?
Yes. You can set the Privacy Status to "Private" and use the `publishAt` parameter in the YouTube node, providing a valid ISO 8601 timestamp for when the video should go live.

### How do I handle YouTube's daily upload limits?
The YouTube Data API v3 has a default limit of 100 `videos.insert` calls per day, though the total quota units (10,000) usually limit a standard project to fewer uploads. If you need to post more frequently, you must apply for a quota extension through the Google Cloud Console.

Building a **how to auto post youtube shorts with n8n workflow** can turn content distribution into a more manageable system. By centralizing your files and automating the API interactions, you can maintain a consistent channel presence.

**Related:** [Automate Pinterest Video Pins with n8n: Free Template](/ai-blog-factory/blog/automate-pinterest-video-pins-n8n/)

**Related:** [Automate Social Media Posts with n8n and ChatGPT](/ai-blog-factory/blog/automate-social-media-posts-n8n-chatgpt/)

**Related:** [How to Build an Automated Content Repurposing Workflow in n8n](/ai-blog-factory/blog/build-automated-content-repurposing-workflow-n8n/)

**Related:** [How to Build Automated YouTube Workflow in n8n (Free)](/ai-blog-factory/blog/n8n-automated-youtube-workflow/)
