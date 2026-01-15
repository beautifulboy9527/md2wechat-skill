# CLI Commands Reference

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

# Generate AI image (requires IMAGE_API_KEY)
md2wechat generate_image "A cute cat sitting on a windowsill"

# Initialize config
md2wechat config init

# Show config
md2wechat config show
```
