# Complete Examples

## Example 1: Simple Article (No Images)

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

## Example 2: Article with Local Images

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

## Example 3: AI Mode with Theme

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

## Example 4: AI Image Generation via Natural Language

**User Request:**
```
"Help me add a product concept image at the beginning of article.md"
```

**Process:**
1. Read article.md to understand the product
2. Create an appropriate image prompt based on context
3. Confirm with user: "I'll use this prompt: '...'"
4. Insert `![Product Concept](__generate:...)` at line 2
5. Run conversion command to generate and upload

**Result:** Image generated and uploaded to WeChat

---

## Example 5: Article with Pre-written Image Syntax

**Input**: `mixed.md`
```markdown
# Tech Review

![Product Photo](./product.jpg)

![Comparison Chart](https://example.com/chart.png)

![Concept Art](__generate:Futuristic gadget design__)
```

**Process:**
1. Process 3 images in order
2. Each returns WeChat URL
3. Replace all placeholders
4. Final HTML with all WeChat-hosted images
