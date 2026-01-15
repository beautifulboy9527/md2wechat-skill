---
name: md2wechat
description: Converts Markdown articles to WeChat Official Account formatted HTML with styled CSS and optionally uploads to draft box. Supports API mode for quick conversion and AI mode for beautiful themed layouts (autumn-warm, spring-fresh, ocean-calm). Use when user wants to convert markdown to WeChat article, publish to WeChat, or format articles for WeChat Official Account.
---

# MD to WeChat

Converts Markdown articles to WeChat Official Account formatted HTML with inline CSS and optionally uploads to draft box. Supports two modes:

- **API Mode**: Fast conversion using md2wechat.cn API
- **AI Mode**: Beautiful themed layouts powered by Claude AI

## When to use this skill

- Use this when the user wants to convert a Markdown file to a WeChat Official Account compatible HTML format.
- Use this when the user wants to publish or upload an article to WeChat Draft Box.
- Use this when the user wants to generate AI images for their article or standalone usage.
- Use this when the user mentions "WeChat", "Official Account", "gongzhonghao", or "article formatting".

## How to use it

### Quick Start

```bash
# Preview HTML (API mode, fast)
bash skill/md2wechat/scripts/run.sh convert article.md --preview

# Preview HTML (AI mode, themed)
bash skill/md2wechat/scripts/run.sh convert article.md --mode ai --theme autumn-warm --preview

# Upload to WeChat draft box
bash skill/md2wechat/scripts/run.sh convert article.md --draft --cover cover.jpg
```

### Natural Language Image Generation

You can also ask me to generate images using natural language:

#### Generate Image for Article (Insert into Markdown)

```
"Help me generate a product concept image at the beginning of article.md"
"Add an image showing the product features after the second paragraph"
"Create a diagram for the comparison section in article.md"
```

I will:
1. Read the article to understand the context
2. Insert the AI image generation syntax at the appropriate location
3. Call the conversion command to generate and upload the image

#### Generate Standalone Image (Not for Article)

```
"Generate an image of a cute cat sitting on a windowsill"
"Create a product concept image: modern smart home device, white design"
"Make a diagram showing the user flow"
```

I will:
1. Call the image generation command directly
2. Return the generated image URL and WeChat material ID

### Workflow Checklist

Copy this checklist to track progress:

```
Progress:
- [ ] Step 1: Analyze Markdown structure and images
- [ ] Step 2: Confirm conversion mode (API/AI) and theme
- [ ] Step 3: Generate HTML with inline CSS
- [ ] Step 4: Process images (upload to WeChat)
- [ ] Step 5: Replace image URLs in HTML
- [ ] Step 6: Preview or upload to draft
```

---

### Step 1: Analyze Markdown

Read the markdown file and extract:

| Element | How to Extract |
|---------|----------------|
| **Title** | First `# heading` or filename |
| **Author** | Look for `Author:` or `作者:` in frontmatter |
| **Digest** | First paragraph or generate from content (max 120 chars) |
| **Images** | Collect all `![alt](src)` references |
| **Structure** | Headings, lists, code blocks, quotes, tables |

**Image Reference Types**:

| Type | Syntax | Processing |
|------|--------|------------|
| Local | `![alt](./path/image.png)` | Upload to WeChat |
| Online | `![alt](https://example.com/image.png)` | Download then upload |
| AI Generate | `![alt](__generate:prompt__)` | Generate via AI then upload |

---

### Step 2: Confirm Mode and Theme

#### Conversion Mode

| Mode | Speed | Style | Best For |
|------|-------|-------|----------|
| **API** | Fast (seconds) | Clean, standard | Quick publishing, technical content |
| **AI** | Slower (10-30s) | Beautiful themed | Important articles, brand content |

#### AI Themes

| Theme | Description | Best For |
|-------|-------------|----------|
| **autumn-warm** | Warm orange tones, emotional, literary | Stories, lifestyle, essays |
| **spring-fresh** | Fresh green tones, natural, vibrant | Travel, nature, outdoor |
| **ocean-calm** | Calm blue tones, professional, rational | Tech articles, business analysis |
| **custom** | Use custom prompt | Brand customization |

#### API Themes (Fast)

| Theme | Description | Best For |
|-------|-------------|----------|
| **default** | Default theme, clean and professional | General content |
| **bytedance** | ByteDance style | Tech news |
| **apple** | Apple minimalist style | Product reviews |
| **sports** | Active sports style | Sports content |
| **chinese** | Traditional Chinese culture style | Cultural articles |
| **cyber** | Cyberpunk style | Frontier tech |

**Ask the user**: "Which mode and theme would you like?"

- **API mode** (fast): default, bytedance, apple, sports, chinese, cyber
- **AI mode** (themed): autumn-warm, spring-fresh, ocean-calm

**Default**: Use `API mode` if user doesn't specify.

Read detailed style prompts from [references/themes.md](references/themes.md)

---

### Step 3: Generate HTML

#### API Mode

Call md2wechat CLI:

```bash
bash skill/md2wechat/scripts/run.sh convert article.md --mode api
```

#### AI Mode

Read the selected style prompt from `references/themes.md` and generate HTML with **inline CSS**.

**Important Rules**:

1. All CSS must be **inline** (in `style` attributes)
2. No external stylesheets or scripts
3. Use WeChat-safe HTML tags only
4. Image placeholder format: `<!-- IMG:0 -->`, `<!-- IMG:1 -->`, etc.

**Safe HTML Tags**:
- `<p>`, `<br>`, `<strong>`, `<em>`, `<u>`, `<a>`
- `<h1>` to `<h6>`
- `<ul>`, `<ol>`, `<li>`
- `<blockquote>`, `<pre>`, `<code>`
- `<table>`, `<thead>`, `<tbody>`, `<tr>`, `<th>`, `<td>`
- `<section>`, `<span>` (with inline styles)

**Avoid**:
- `<script>`, `<iframe>`, `<form>`
- External CSS/JS references
- Complex positioning (fixed, absolute)

**Critical for WeChat**:
- Create a main `<div>` container immediately after `<body>` to hold all global styles
- Specify `color` explicitly for each `<p>` tag (WeChat resets to black otherwise)
- Use two `<span>` tags for heading symbols: one with color+text-shadow, one with solid color

---

### Step 4: Process Images

#### Image Generation Methods

There are **three ways** to generate AI images:

**Method 1: Natural Language - For Article (Recommended)**

Simply describe what you want in plain language:

```
User: "Generate a product concept image at the beginning of article.md"

User: "Add a comparison chart after the third paragraph"

User: "Create an image showing the workflow diagram in article.md"
```

**How I process natural language requests:**

1. **Understand the intent** - Identify where to insert the image
2. **Read the article** - Analyze context to create an appropriate prompt
3. **Insert the syntax** - Add `![alt](__generate:prompt__)` at the correct location
4. **Confirm with user** - Show the prompt I created and ask for approval
5. **Generate and upload** - Call the conversion command to complete

**Method 2: Natural Language - Standalone Image**

Generate an image without any article:

```
User: "Generate an image of a cute cat sitting on a windowsill"
User: "Create a product concept: modern smart home device"
User: "Make a diagram showing user signup flow"
```

**I will:**
1. Create an appropriate prompt based on your description
2. Call: `bash skill/md2wechat/scripts/run.sh generate_image "prompt"`
3. Return the WeChat URL and media ID

**Use when:** You just need an image, not for any article.

**Method 3: Manual Syntax**

Write the image generation syntax directly in Markdown:

```markdown
![Product Concept](__generate:A futuristic smart home hub device, sleek design__)
```

**Syntax format:** `![alt text](__generate:prompt__)`

---

#### Processing Images by Type

For each image reference in order:

**Local Image**

```bash
bash skill/md2wechat/scripts/run.sh upload_image "/path/to/image.png"
```

Response:
```json
{"success": true, "wechat_url": "https://mmbiz.qpic.cn/...", "media_id": "xxx"}
```

**Online Image**

```bash
bash skill/md2wechat/scripts/run.sh download_and_upload "https://example.com/image.png"
```

**AI Generated Image (via CLI)**

```bash
bash skill/md2wechat/scripts/run.sh generate_image "A cute cat sitting on a windowsill"
```

**Note**: AI image generation requires `IMAGE_API_KEY` environment variable.

**Image Processing Pipeline**:
1. If AI generation: Call image API → get URL
2. If online: Download image to temp
3. If local: Read file
4. Compress if width > 1920px (configurable)
5. Upload to WeChat material API
6. Return `wechat_url` and `media_id`
7. Store result for HTML replacement

---

### Step 5: Replace Image URLs

Replace placeholders in HTML:

```html
<!-- Before -->
<!-- IMG:0 -->
<!-- IMG:1 -->

<!-- After -->
<img src="https://mmbiz.qpic.cn/..." />
<img src="https://mmbiz.qpic.cn/..." />
```

Use the WeChat URLs returned from image processing.

---

### Step 6: Preview or Upload

Ask user:

1. **Preview only** - Show HTML for review
2. **Upload to draft** - Create WeChat draft article

#### Preview Mode

Display HTML in markdown code block for user to copy.

#### Upload Mode

Create draft and run:

```bash
bash skill/md2wechat/scripts/run.sh convert article.md --draft --cover cover.jpg
```

**Required for draft**:
- `WECHAT_APPID` environment variable
- `WECHAT_SECRET` environment variable
- Cover image (use `--cover` or first image in content)

Response:
```json
{"success": true, "media_id": "draft_media_id", "draft_url": "https://mp.weixin.qq.com/..."}
```

---

## Configuration

### Required for WeChat API

| Variable | Description | Required |
|----------|-------------|----------|
| `WECHAT_APPID` | WeChat Official Account AppID | Yes, for draft upload |
| `WECHAT_SECRET` | WeChat API Secret | Yes, for draft upload |

### Optional for AI Features

| Variable | Description | Required |
|----------|-------------|----------|
| `IMAGE_API_KEY` | Image generation API key | For AI images |
| `IMAGE_API_BASE` | Image API base URL | For AI images |
| `COMPRESS_IMAGES` | Compress images > 1920px (true/false) | No, default true |
| `MAX_IMAGE_WIDTH` | Max width in pixels | No, default 1920 |

### How to Get AppID and Secret

1. Visit [WeChat Developer Platform](https://developers.weixin.qq.com/platform)
2. Login and select your Official Account
3. Go to **Settings & Development** → **Basic Configuration**
4. Find in **Developer ID** section:
   - **Developer ID (AppID)**: Copy directly
   - **Developer Password (AppSecret)**: Click "Reset" to get
5. Add these values to environment variables or config file

> **Warning**: AppSecret is very important, keep it secure!

### Config File Location

```
~/.config/md2wechat/config.yaml    # Global config
./md2wechat.yaml                    # Project config (higher priority)
```

---

## Error Handling

| Error | Action |
|-------|--------|
| Missing config | Ask user to set environment variable or run `md2wechat config init` |
| Image upload fails | Log error, continue with placeholder |
| WeChat API fails | Show error message, return HTML for manual upload |
| Markdown parse error | Ask user to check file format |
| IP not in whitelist | Guide user to add IP to WeChat whitelist (see Troubleshooting) |

---

## References

- [Style Themes](references/themes.md) - Detailed style prompts for AI themes
- [HTML Guide](references/html-guide.md) - WeChat HTML constraints and best practices
- [Image Syntax](references/image-syntax.md) - Image reference syntax
- [WeChat API](references/wechat-api.md) - API reference
- [Complete Examples](references/examples.md) - Usage examples
- [Troubleshooting](references/troubleshooting.md) - Common issues and solutions
- [CLI Reference](references/cli.md) - Command line interface reference
