---
name: md2wechat
description: Converts Markdown articles to WeChat Official Account formatted HTML with styled CSS, AI-generated images, and automatic uploading.
---

# MD to WeChat Skill

This skill converts Markdown content into WeChat Official Account compatible HTML, supporting rich styling, AI image generation, and direct uploading to WeChat Drafts.

## 🧠 AI Usage Instructions

**When to use:**
- User wants to format/publish an article to WeChat.
- User wants to generate images or charts for an article.
- User mentions "WeChat", "Official Account", "gongzhonghao".

**How to use:**
1.  **Write Markdown**: Create a markdown file with the user's content.
2.  **Add Assets (Optional)**:
    *   **AI Images**: Use `![alt](__generate:prompt|size=16:9__)` to generate images.
    *   **Charts/Viz**: Use `![alt](__html_base64:encoded_html__)` (Advanced) or rely on the tool's auto-generation features.
    *   **Prompt Cards**: Use standard code blocks with "Prompt:" or "提示词:" to automatically style them as cards.
3.  **Run Build Script**: Execute `python skill/md2wechat/scripts/build.py <file> --upload`.

## 📝 Markdown Syntax for AI

### 1. Frontmatter Configuration
Always check if the user wants a specific theme or cover.

```markdown
---
theme: chinese-scroll  # Options: default, chinese-scroll, fashion-bold, ocean-calm, twilight
cover:
  prompt: "A beautiful landscape"
  style: art
---
```

### 2. AI Image Generation
To insert an AI-generated image, use the `__generate:` prefix in the image source.

*   **Syntax**: `![Description](__generate:Your Prompt Here|size=16:9__)`
*   **Example**: `![A cat](__generate:A cute cat sitting on a window|size=16:9__)`
*   **Supported Sizes**: `16:9` (default), `1:1`, `9:16`.

### 3. Prompt/Code Cards
The tool automatically detects code blocks that look like prompts and styles them as "Cards".

*   **Trigger**: Code block content containing "Prompt:", "提示词:", or "ContentAny".
*   **Example**:
    ```markdown
    ```text
    Prompt: A futuristic city
    1. High detail
    2. Neon lights
    ```
    ```

## 🚀 Command Reference

### Build & Upload
```bash
python skill/md2wechat/scripts/build.py <input_file.md> --upload
```

### Preview Only (No Upload)
```bash
python skill/md2wechat/scripts/build.py <input_file.md>
```

### Card Mode (Long Image)
Renders the entire article as a series of images (good for posters).
```bash
python skill/md2wechat/scripts/build.py <input_file.md> --mode image --upload
```

## 🎨 Theme List

*   `default`: Clean, standard.
*   `chinese-scroll`: Traditional Chinese style (Ink, Scroll).
*   `fashion-bold`: High contrast, trendy.
*   `ocean-calm`: Blue tones, professional.
*   `twilight`: Dark mode, tech-focused.
*   `autumn-warm`: Warm colors, emotional.

## ⚠️ Important Notes

*   **Privacy**: Do NOT upload `md2wechat.yaml` or any credentials to Git.
*   **Assets**: Generated images are stored in `assets/generated/`.
*   **WeChat Limits**: Images > 10MB may fail. The tool attempts to compress them.
