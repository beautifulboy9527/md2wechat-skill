import argparse
import os
import sys
import yaml
import re
import subprocess
import shutil

# Add scripts dir to path
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SCRIPTS_DIR)

import generate_image
import render_visual
import append_footer
import python_converter
import wechat_uploader
import slice_image
# We need to import html_to_image, but it's an async script. 
# We can run it via subprocess or use asyncio.run inside build.py if we refactor.
# For simplicity and stability, let's use subprocess for the playwright part as it was designed as a script.
import subprocess




def parse_frontmatter(content):
    """
    Extracts YAML frontmatter from markdown content.
    Returns (frontmatter_dict, markdown_body)
    """
    frontmatter_regex = re.compile(r'^---\s*\n(.*?)\n---\s*\n', re.DOTALL)
    match = frontmatter_regex.match(content)
    
    if match:
        yaml_content = match.group(1)
        try:
            config = yaml.safe_load(yaml_content)
            body = content[match.end():]
            return config, body
        except yaml.YAMLError as e:
            print(f"Warning: Failed to parse Frontmatter: {e}")
            return {}, content
    
    return {}, content

def load_global_config():
    """Load md2wechat.yaml from CWD or Home"""
    paths = [
        os.path.join(os.getcwd(), "md2wechat.yaml"),
        os.path.join(os.path.expanduser("~"), ".md2wechat.yaml")
    ]
    for p in paths:
        if os.path.exists(p):
            with open(p, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
    return {}

def build_article(input_file, output_file=None, upload=False, mode="text", platform="wechat"):
    if not os.path.exists(input_file):
        print(f"Error: File {input_file} not found.")
        return

    print(f"🔨 Building {input_file} for [{platform.upper()}] in [{mode.upper()}] mode...")



    # 0. Load Global Config
    global_config = load_global_config()

    # 1. Read Content & Parse Frontmatter
    with open(input_file, 'r', encoding='utf-8') as f:
        raw_content = f.read()
    
    fm_config, body_content = parse_frontmatter(raw_content)
    
    # Merge configs (Frontmatter overrides Global)
    config = global_config.copy()
    config.update(fm_config)
    
    # Platform-specific defaults
    if platform == "xhs":
        theme = config.get("theme", "xhs-card")
    else:
        theme = config.get("theme", "default")

    
    # Determine Output Filename
    if not output_file:
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        if platform == "xhs":
            output_file = f"{base_name}_xhs.html"
        else:
            output_file = f"{base_name}_wechat.html"
    
    # 3. Asset Generation (Pre-processing)
    # Check for Cover Generation
    # 3. Asset Generation (Pre-processing)
    # Check for Cover Generation
    cover_config = config.get("cover")
    final_cover_path = None

    if cover_config:
        if isinstance(cover_config, str):
            final_cover_path = cover_config
            print(f"✅ Using provided cover path: {final_cover_path}")
        elif isinstance(cover_config, dict):
            if cover_config.get("path"):
                final_cover_path = cover_config.get("path")
                print(f"✅ Using provided cover path: {final_cover_path}")
            else:
                print("🎨 Generating Cover Image...")
                prompt = cover_config.get("prompt", "A nice cover image")
                style = cover_config.get("style", None)
                sub_style = cover_config.get("sub_style", None)
                size = cover_config.get("size", "16:9") # Default to 16:9 for cover
                cover_path = "cover.jpg" 
                
                try:
                    # Generate local cover file
                    generate_image.generate_image_file(prompt, cover_path, style, sub_style, size)
                    print(f"✅ Cover generated: {cover_path}")
                    final_cover_path = cover_path
                except Exception as e:
                    print(f"⚠️ Cover generation failed: {e}") 

    # 3. Conversion (Markdown -> HTML)
    print(f"📝 Converting Markdown using theme: {theme}...")
    
    themes_dir = os.path.join(os.path.dirname(SCRIPTS_DIR), "../../themes")
    try:
        # python_converter returns a FULL HTML document with inline CSS
        raw_html = python_converter.convert_markdown_to_wechat(body_content, theme, themes_dir)
        
        # 3.5 Asset Processing (New Step)
        # Decoupled generation of AI images and HTML visualizations
        import processor
        asset_processor = processor.AssetProcessor(os.path.dirname(os.path.abspath(input_file)))
        final_html = asset_processor.process(raw_html)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_html)
            
    except Exception as e:
        print(f"❌ Conversion failed: {e}")
        import traceback
        traceback.print_exc()
        return

    # 4. Post-processing (Footer) - Only for text mode or before rendering image
    # If mode is image, we want footer INSIDE the image, so append it to HTML before rendering.
    
    footer_config = config.get("footer")
    if footer_config:
        print("🦶 Appending Footer...")
        # ... (existing footer logic) ...
        # We need to read/write the temp HTML file if we are in image mode, 
        # or the output file if text mode.
        
        # Let's define the html file to work on
        target_html_file = output_file
        
        with open(target_html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
            
        footer_html = append_footer.footer_assets.get_footer(
            footer_config.get("template", "glass_contact"),
            footer_config
        )
        
        if "</body>" in html_content:
            new_content = html_content.replace("</body>", f"{footer_html}\n</body>")
        else:
            new_content = html_content + "\n" + footer_html
            
        with open(target_html_file, 'w', encoding='utf-8') as f:
            f.write(new_content)

    # 5. Handle Image/Card Mode
    final_content_html = "" 
    
    if mode == "image":
        print("📸 Rendering article to Card Images (Section by Section)...")
        
        # 1. Split HTML into sections
        # We need the full HTML first (with footer if configured)
        # Append footer to the HTML content before splitting? 
        # Or handle footer as a separate card? 
        # User wants flexibility. Let's append footer to the main HTML first, then split.
        # But wait, footer usually goes at the end. If we append it, it will likely be in the last section.
        
        # Let's read the current HTML (which might have footer appended from step 4 if we didn't skip it)
        # Actually step 4 appends to output_file.
        with open(output_file, 'r', encoding='utf-8') as f:
            full_html = f.read()
            
        sections = python_converter.split_html_by_sections(full_html, card_mode=True)
        print(f"🔪 Split into {len(sections)} cards.")
        
        card_images = []
        script_path = os.path.join(os.path.dirname(__file__), "html_to_image.py")
        
        # 2. Render each section
        # Platform-specific dimensions
        if platform == "xhs":
            card_width = 1080
            card_height = 1440  # 3:4 ratio for Xiaohongshu
        else:
            card_width = 1080
            card_height = None  # Auto height for WeChat
        
        for i, section_html in enumerate(sections):
            print(f"   Rendering Card {i+1}/{len(sections)}...")
            
            # Platform-specific naming
            if platform == "xhs":
                if i == 0:
                    card_path = f"cover.png"
                else:
                    card_path = f"card_{i}.png"
            else:
                card_path = f"{os.path.splitext(output_file)[0]}_card_{i}.png"
            
            # Write section to temp file for rendering
            temp_card_html = f"temp_card_{i}.html"
            with open(temp_card_html, 'w', encoding='utf-8') as f:
                f.write(section_html)
                
            try:
                # Render with platform-specific dimensions
                cmd = ["python", script_path, temp_card_html, card_path, "--width", str(card_width)]
                if card_height:
                    cmd.extend(["--height", str(card_height)])
                
                subprocess.run(cmd, check=True)
                card_images.append(card_path)
            except subprocess.CalledProcessError:
                print(f"❌ Failed to render Card {i}.")
            finally:
                if os.path.exists(temp_card_html): os.remove(temp_card_html)
        
        # 3. Construct Image-Only HTML
        img_tags = []
        for img_path in card_images:
            rel_path = os.path.relpath(img_path, os.path.dirname(output_file))
            # Use 100% width and no margin to make them look like a continuous stream
            img_tags.append(f'<img src="{rel_path}" style="width: 100%; display: block; margin: 0;">')
            
        final_content_html = "\n".join(img_tags)
        
        # Overwrite output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_content_html)
            
    else:
        # Text mode
        with open(output_file, 'r', encoding='utf-8') as f:
            final_content_html = f.read()


    # 6. Upload to WeChat (Optional)
    if upload:
        app_id = config.get("app_id")
        app_secret = config.get("app_secret")
        
        if not app_id or not app_secret:
            print("⚠️ Cannot upload: app_id or app_secret not found in config (md2wechat.yaml or frontmatter).")
        else:
            print("🚀 Uploading to WeChat...")
            try:
                uploader = wechat_uploader.WeChatUploader(app_id, app_secret)
                
                # A. Upload Cover
                cover_media_id = None
                if final_cover_path and os.path.exists(final_cover_path):
                    print(f"📤 Uploading cover image: {final_cover_path}")
                    cover_media_id, _ = uploader.upload_image(final_cover_path)
                elif cover_config:
                    # Fallback if final_cover_path was not set but cover_config exists (e.g. generation failed)
                    # Try default 'cover.jpg' just in case
                    if os.path.exists("cover.jpg"):
                         print("📤 Uploading default cover.jpg...")
                         cover_media_id, _ = uploader.upload_image("cover.jpg")
                
                # B. Process Content Images (Works for both Text mode and Image mode!)
                # In Image mode, it will find the slice images and upload them.
                
                # IMPORTANT: Strip HTML/HEAD/BODY tags for WeChat upload
                # WeChat expects a fragment, not a full document.
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(final_content_html, 'html.parser')
                if soup.body:
                    upload_content = "".join([str(x) for x in soup.body.contents])
                else:
                    upload_content = final_content_html
                
                processed_html = uploader.process_html_images(upload_content, os.path.dirname(input_file))
                
                # C. Upload Draft
                title = config.get("title")
                if not title:
                    # Try to extract from first H1 in raw markdown (before parsing)
                    # We have raw_content available from earlier
                    h1_match = re.search(r'^#\s+(.+)$', raw_content, re.MULTILINE)
                    if h1_match:
                        title = h1_match.group(1).strip()
                    else:
                        title = os.path.splitext(os.path.basename(input_file))[0]
                
                digest = config.get("digest", "")
                author = config.get("author", "")
                
                media_id = uploader.upload_draft(title, processed_html, cover_media_id, author, digest)
                print(f"✅ Successfully uploaded to WeChat Draft! Media ID: {media_id}")
                
            except Exception as e:
                print(f"❌ Upload failed: {e}")

    print(f"✅ Build Complete! Output: {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build Article from Markdown for WeChat or Xiaohongshu")
    parser.add_argument("input_file", help="Input Markdown file")
    parser.add_argument("--output", help="Output HTML file")
    parser.add_argument("--upload", action="store_true", help="Upload to platform (WeChat Draft or XHS)")
    parser.add_argument("--mode", choices=["text", "image"], default="text", help="Output mode: text (default) or image (card rendering)")
    parser.add_argument("--platform", choices=["wechat", "xhs"], default="wechat", help="Target platform: wechat (default) or xhs (Xiaohongshu)")
    
    args = parser.parse_args()
    build_article(args.input_file, args.output, args.upload, args.mode, args.platform)


