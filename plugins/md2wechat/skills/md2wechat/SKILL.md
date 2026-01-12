---
name: md2wechat
description: Convert Markdown articles to WeChat Official Account formatted HTML with styled CSS and optionally upload to draft box. Supports API mode for quick conversion and AI mode for beautiful themed layouts (autumn-warm, spring-fresh, ocean-calm). Use when user wants to convert markdown to WeChat article, publish to WeChat, or format articles for WeChat Official Account.
---

# MD to WeChat

Converts Markdown articles to WeChat Official Account formatted HTML with inline CSS and optionally uploads to draft box. Supports two modes:

- **API Mode**: Fast conversion using md2wechat.cn API
- **AI Mode**: Beautiful themed layouts powered by Claude AI

## Quick Start

```bash
# Preview HTML (API mode, fast)
bash skill/md2wechat/scripts/run.sh convert article.md --preview

# Preview HTML (AI mode, themed)
bash skill/md2wechat/scripts/run.sh convert article.md --mode ai --theme autumn-warm --preview

# Upload to WeChat draft box
bash skill/md2wechat/scripts/run.sh convert article.md --draft --cover cover.jpg
```

## Workflow Checklist

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

## Step 1: Analyze Markdown

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

## Step 2: Confirm Mode and Theme

### Conversion Mode

| Mode | Speed | Style | Best For |
|------|-------|-------|----------|
| **API** | Fast (seconds) | Clean, standard | Quick publishing, technical content |
| **AI** | Slower (10-30s) | Beautiful themed | Important articles, brand content |

### AI Themes

| Theme | Description | Best For |
|-------|-------------|----------|
| **autumn-warm** | Warm orange tones, emotional, literary | Stories, lifestyle, essays |
| **spring-fresh** | Fresh green tones, natural, vibrant | Travel, nature, outdoor |
| **ocean-calm** | Calm blue tones, professional, rational | Tech articles, business analysis |
| **custom** | Use custom prompt | Brand customization |

### API Themes (Fast)

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

## Step 3: Generate HTML

### API Mode

Call md2wechat CLI:

```bash
bash skill/md2wechat/scripts/run.sh convert article.md --mode api
```

### AI Mode

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

## Step 4: Process Images

For each image reference in order:

### Local Image

```bash
bash skill/md2wechat/scripts/run.sh upload_image "/path/to/image.png"
```

Response:
```json
{"success": true, "wechat_url": "https://mmbiz.qpic.cn/...", "media_id": "xxx"}
```

### Online Image

```bash
bash skill/md2wechat/scripts/run.sh download_and_upload "https://example.com/image.png"
```

### AI Generated Image

```bash
bash skill/md2wechat/scripts/run.sh generate_image "A cute cat sitting on a windowsill"
```

**Note**: Requires `IMAGE_API_KEY` environment variable.

**Image Processing Pipeline**:
1. If AI generation: Call image API → get URL
2. If online: Download image to temp
3. If local: Read file
4. Compress if width > 1920px (configurable)
5. Upload to WeChat material API
6. Return `wechat_url` and `media_id`
7. Store result for HTML replacement

---

## Step 5: Replace Image URLs

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

## Step 6: Preview or Upload

Ask user:

1. **Preview only** - Show HTML for review
2. **Upload to draft** - Create WeChat draft article

### Preview Mode

Display HTML in markdown code block for user to copy.

### Upload Mode

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

## Complete Examples

### Example 1: Simple Article (No Images)

**Input**: `simple.md`
```markdown
# My First Article

This is a simple article with no images.
```

**Process**:
1. Generate HTML with API mode
2. Skip image processing
3. Ask: preview or upload?
4. If upload → create draft

### Example 2: Article with Local Images

**Input**: `with-images.md`
```markdown
# Travel Diary

Day 1 in Paris:

![Eiffel Tower](./photos/eiffel.jpg)
```

**Process**:
1. Analyze: 1 local image
2. Generate HTML with `<!-- IMG:0 -->` placeholder
3. Run: `upload_image "./photos/eiffel.jpg"`
4. Replace placeholder with WeChat URL
5. Preview or upload

### Example 3: AI Mode with Theme

**Input**: `story.md`
```markdown
# The Old Library

A story about memories...
```

**Process**:
1. User selects AI mode + autumn-warm theme
2. Read theme prompt from references/themes.md
3. Generate themed HTML with inline CSS
4. Preview or upload

### Example 4: Mixed Image Types

**Input**: `mixed.md`
```markdown
# Tech Review

![Product Photo](./product.jpg)

![Comparison Chart](https://example.com/chart.png)

![Concept Art](__generate:Futuristic gadget design__)
```

**Process**:
1. Process 3 images in order
2. Each returns WeChat URL
3. Replace all placeholders
4. Final HTML with all WeChat-hosted images

---

## References

- [Style Themes](references/themes.md) - Detailed style prompts for AI themes
- [HTML Guide](references/html-guide.md) - WeChat HTML constraints and best practices
- [Image Syntax](references/image-syntax.md) - Image reference syntax
- [WeChat API](references/wechat-api.md) - API reference

---

## Troubleshooting

### Configuration Issues

**Q: "AppID not configured" error**
A: Set `WECHAT_APPID` and `WECHAT_SECRET` environment variables, or run:
```bash
md2wechat config init
```

**Q: Config file not working**
A: Check config file location. Supported locations:
- `./md2wechat.yaml` (current directory, highest priority)
- `~/.md2wechat.yaml`
- `~/.config/md2wechat/config.yaml`

### Image Issues

**Q: Image upload fails with "invalid filetype"**
A: WeChat supports JPG, PNG, GIF. Ensure image is in correct format:
```bash
# Convert using ImageMagick
convert input.tiff output.jpg
```

**Q: Images not showing in draft**
A: Images must use WeChat-hosted URLs (`mmbiz.qpic.cn`), not external URLs.

**Q: AI image generation fails**
A: Check `IMAGE_API_KEY` is set and API base URL is correct.

### WeChat API Issues

**Q: "IP not in whitelist" error**
A: Add your server IP to WeChat whitelist:

1. Get your public IP:
```bash
curl ifconfig.me
# or
curl ip.sb
```

2. Add IP to WeChat:
   - Visit [WeChat Developer Platform](https://developers.weixin.qq.com/platform)
   - Go to **Settings & Development** → **Basic Configuration**
   - Find **IP Whitelist** section
   - Click "Set" and add your IP
   - Wait a few minutes for changes to take effect

**Q: "access_token expired" error**
A: Program auto-refreshes tokens. If persists:
```bash
# Check config
md2wechat config show

# Re-init if needed
md2wechat config init
```

**Q: "create draft failed" error**
A: Possible causes:
1. Insufficient permissions - ensure account is verified
2. Sensitive content - check article content
3. Draft limit reached - check existing drafts

**Q: API rate limit exceeded**
A: WeChat has API limits. Wait and retry:
```bash
# Wait 60 seconds
sleep 60
# Retry
md2wechat convert article.md --draft
```

### HTML/Style Issues

**Q: Styles not working in WeChat editor**
A: Check:
1. CSS uses inline `style` attributes (not `<style>` tags)
2. CSS properties are in allowed list (see HTML Guide)
3. No syntax errors (unclosed tags, etc.)

**Q: Background color lost in WeChat**
A: WeChat strips `<body>` styles. Use main container:
```html
<div style="background-color: #faf9f5; padding: 40px 10px;">
  <!-- All content here -->
</div>
```

**Q: Text color not as expected**
A: WeChat resets `<p>` color to black. Always specify:
```html
<p style="color: #4a413d;">Your text here</p>
```

### Command Issues

**Q: "command not found: md2wechat"**
A: Binary not in PATH. Use full path or add to PATH:
```bash
# Use full path
./bin/md2wechat-linux-amd64 --help

# Or add to PATH
export PATH=$PATH:/path/to/md2wechat/bin
```

**Q: AI mode very slow**
A: AI mode requires Claude API call and takes 10-30 seconds. For faster results, use API mode.

---

## CLI Commands Reference

```bash
# Show help
md2wechat --help

# Convert and preview
md2wechat convert article.md --preview

# Convert with AI theme
md2wechat convert article.md --mode ai --theme autumn-warm --preview

# Convert and upload to draft
md2wechat convert article.md --draft --cover cover.jpg

# Upload single image
md2wechat upload_image photo.jpg

# Download and upload online image
md2wechat download_and_upload https://example.com/image.jpg

# Initialize config
md2wechat config init

# Show config
md2wechat config show
```
