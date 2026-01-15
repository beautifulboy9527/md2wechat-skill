# Troubleshooting

## Configuration Issues

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

## Image Issues

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

## WeChat API Issues

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

## HTML/Style Issues

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

## Command Issues

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
