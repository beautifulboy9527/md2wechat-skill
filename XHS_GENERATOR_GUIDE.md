# Xiaohongshu & Multi-Style Graphic Generator Update

We have successfully updated the `md2wechat-skill` to support multiple new graphic styles, specifically tailored for Xiaohongshu (Little Red Book) and other modern aesthetic requirements.

## New Styles Added

The following styles have been integrated into the `style_prompts.py` library and are available for use in image generation and HTML card rendering.

### 1. Xiaohongshu Info Card (`xhs-note`)
*   **Style Key:** `xhs`
*   **Description:** Vertical 9:16 layout with glassmorphism effects, Morandi color palette, and clear information hierarchy.
*   **Usage:** Ideal for knowledge cards, tips, and quick summaries.
*   **Features:**
    *   Gradient background (Pink/Blue/Mint)
    *   Glass-effect card container
    *   "Core Knowledge" subtitle decoration
    *   Optimized for mobile viewing

### 2. Vintage Didactic Journal (`vintage-journal`)
*   **Style Key:** `vintage`
*   **Description:** Retro academic style simulating old paper, handwritten notes, and scholarly aesthetics.
*   **Usage:** Great for history, literature, or "deep dive" technical content.
*   **Features:**
    *   Textured paper background
    *   Serif fonts mixed with handwritten script
    *   "Approved" stamp decoration
    *   Double-border headers

### 3. Memphis Pop (`memphis-pop`)
*   **Style Key:** `memphis`
*   **Description:** High-energy, bold geometric style with vibrant colors and high contrast.
*   **Usage:** Perfect for trends, announcements, and grabbing attention.
*   **Features:**
    *   Bold geometric shapes (circles, triangles)
    *   Vibrant colors (Yellow, Blue, Pink)
    *   Pop-art inspired layout
    *   Dynamic shadows

## How to Use

### In Markdown Frontmatter
You can apply these styles by setting the `theme` in your markdown file's frontmatter:

```yaml
---
title: My Awesome Post
theme: xhs-note  # or 'vintage-journal', 'memphis-pop'
---
```

### In Image Generation Prompts
You can also use the new sub-styles in your image generation prompts:

*   **Tech:** `hologram`
*   **Art:** `washi`, `paper_cut`
*   **Retro:** `mosaic`
*   **Nature:** `stardust`

Example:
```markdown
![A futuristic city](__generate:A futuristic city|style=tech|sub_style=hologram__)
```

### Using the Render Script Directly
You can generate these cards programmatically using `render_visual.py`:

```bash
python skill/md2wechat/scripts/render_visual.py html "Your content here" output.png --style xhs --title "Title"
```
