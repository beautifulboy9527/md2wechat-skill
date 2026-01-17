import os
import sys
import subprocess
from PIL import Image, ImageDraw, ImageFont

# Try to import generate_image for AI mode
try:
    from generate_image import generate_image_file
except ImportError:
    generate_image_file = None

def generate_html_cover(title, digest, output_path, width=900, height=383):
    """
    Generates a cover image using HTML/CSS and playwright (via screenshot).
    Simplified design: Title + Decoration + Tag.
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("⚠️ Playwright not installed. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright"])
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
        from playwright.sync_api import sync_playwright

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;700;900&display=swap');
            
            body {{
                margin: 0; padding: 0;
                width: {width}px; height: {height}px;
                background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
                font-family: 'Noto Sans SC', 'Microsoft YaHei', sans-serif;
                display: flex;
                justify-content: center;
                align_items: center;
                overflow: hidden;
                position: relative;
            }}
            
            /* Decorative Background Blobs */
            .blob {{
                position: absolute;
                border-radius: 50%;
                filter: blur(40px);
                opacity: 0.6;
                z-index: 0;
            }}
            .blob-1 {{ top: -50px; left: -50px; width: 300px; height: 300px; background: #ff00cc; }}
            .blob-2 {{ bottom: -50px; right: -50px; width: 350px; height: 350px; background: #333399; }}
            .blob-3 {{ top: 50%; left: 50%; transform: translate(-50%, -50%); width: 200px; height: 200px; background: #00ccff; opacity: 0.4; }}

            .card {{
                position: relative;
                z-index: 1;
                width: 85%;
                height: 70%;
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(16px);
                -webkit-backdrop-filter: blur(16px);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 20px;
                box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
                display: flex;
                flex-direction: column;
                justify-content: center;
                align_items: center;
                padding: 40px;
                text-align: center;
            }}
            
            h1 {{
                font-size: 52px;
                font-weight: 900;
                margin: 0 0 20px 0;
                line-height: 1.2;
                color: #ffffff;
                text-shadow: 0 2px 10px rgba(0,0,0,0.3);
                letter-spacing: 1px;
            }}
            
            .subtitle {{
                font-size: 24px;
                color: rgba(255, 255, 255, 0.9);
                font-weight: 400;
                margin-bottom: 30px;
                max-width: 80%;
                line-height: 1.4;
            }}

            .tag-container {{
                display: flex;
                gap: 15px;
            }}
            
            .tag {{
                font-size: 16px;
                color: #ffffff;
                background: rgba(255, 255, 255, 0.2);
                padding: 8px 20px;
                border-radius: 50px;
                font-weight: 700;
                border: 1px solid rgba(255, 255, 255, 0.3);
                text-transform: uppercase;
                letter-spacing: 1px;
                display: flex;
                align-items: center;
            }}
            
            .tag::before {{
                content: '';
                display: inline-block;
                width: 8px;
                height: 8px;
                background: #00ffcc;
                border-radius: 50%;
                margin-right: 8px;
                box-shadow: 0 0 10px #00ffcc;
            }}
        </style>
    </head>
    <body>
        <div class="blob blob-1"></div>
        <div class="blob blob-2"></div>
        <div class="blob blob-3"></div>
        
        <div class="card">
            <h1>{title}</h1>
            <div class="subtitle">{digest if digest else "深度解析与实战指南"}</div>
            <div class="tag-container">
                <div class="tag">AI 创作</div>
                <div class="tag">自媒体运营</div>
            </div>
        </div>
    </body>
    </html>
    """
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': width, 'height': height})
        page.set_content(html)
        page.screenshot(path=output_path)
        browser.close()
    
    return output_path

def generate_cover(title, digest="", mode="html", ip_style="tech", output_path="cover.jpg"):
    print(f"🎨 Generating cover for '{title}' (Mode: {mode})...")
    
    if mode == "ai" and generate_image_file:
        # AI Mode logic (omitted for brevity, using HTML for now as requested)
        pass
        
    # Default to HTML mode
    return generate_html_cover(title, digest, output_path)

if __name__ == "__main__":
    generate_cover("测试标题", "测试摘要", output_path="test_cover.jpg")
