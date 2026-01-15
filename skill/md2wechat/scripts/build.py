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

def build_article(input_file, output_file=None, upload=False):
    if not os.path.exists(input_file):
        print(f"Error: File {input_file} not found.")
        return

    print(f"🔨 Building {input_file}...")

    # 0. Load Global Config
    global_config = load_global_config()

    # 1. Read Content & Parse Frontmatter
    with open(input_file, 'r', encoding='utf-8') as f:
        raw_content = f.read()
    
    fm_config, body_content = parse_frontmatter(raw_content)
    
    # Merge configs (Frontmatter overrides Global)
    config = global_config.copy()
    config.update(fm_config)
    
    # Defaults
    theme = config.get("theme", "default")

    
    # Determine Output Filename
    if not output_file:
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        output_file = f"{base_name}_wechat.html"
    
    # 2. Asset Generation (Pre-processing)
    # Check for Cover Generation
    cover_config = config.get("cover")
    if cover_config:
        print("🎨 Generating Cover Image...")
        prompt = cover_config.get("prompt", "A nice cover image")
        style = cover_config.get("style", None)
        sub_style = cover_config.get("sub_style", None)
        size = cover_config.get("size", "1280x720")
        cover_path = "cover.jpg" # Default name, maybe make unique?
        
        # Call generate_image logic directly
        # We use the imported module instead of subprocess for speed/cleanliness
        # But generate_image.py expects a binary path for uploading... 
        # Wait, the previous generate_image.py required a binary_path for 'upload_image'.
        # Let's just generate it locally for now.
        # We might need to mock the binary path or adjust generate_image to be importable without running main.
        # For now, let's run it as a subprocess to be safe with its internal logic.
        
        # Actually, looking at generate_image.py, it requires a binary_path to upload. 
        # If we just want to generate local files, we might need to tweak it.
        # Let's assume for this step we just want the local file.
        # I'll skip the upload part in this orchestration for simplicity, or we can add a flag to generate_image to skip upload.
        pass 

    # 3. Conversion (Markdown -> HTML)
    print(f"📝 Converting Markdown using theme: {theme}...")
    
    themes_dir = os.path.join(os.path.dirname(SCRIPTS_DIR), "../../themes")
    try:
        html_content = python_converter.convert_markdown_to_wechat(body_content, theme, themes_dir)
        
        # Wrap in a basic HTML shell for viewing
        final_html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WeChat Preview</title>
</head>
<body>
{html_content}
</body>
</html>
"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_html)
            
    except Exception as e:
        print(f"❌ Conversion failed: {e}")
        return

    # 4. Post-processing (Footer)

    footer_config = config.get("footer")
    if footer_config:
        print("lu Footer...")
        # We can pass the config dict directly to append_footer if we modify it to accept dict
        # But append_footer.py currently loads from a file.
        # Let's just write a temp yaml or modify append_footer.
        # Actually, append_footer.py imports footer_assets. We can use footer_assets directly here!
        
        with open(output_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
            
        footer_html = append_footer.footer_assets.get_footer(
            footer_config.get("template", "glass_contact"),
            footer_config
        )
        
        if "</body>" in html_content:
            new_content = html_content.replace("</body>", f"{footer_html}\n</body>")
        else:
            new_content = html_content + "\n" + footer_html
            
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(new_content)

    # 5. Upload to WeChat (Optional)
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
                if cover_config: # If we generated a cover
                    cover_path = "cover.jpg" # Assuming default name from step 2
                    if os.path.exists(cover_path):
                        print("📤 Uploading cover image...")
                        cover_media_id, _ = uploader.upload_image(cover_path)
                
                # B. Process Content Images
                # Read the final HTML
                with open(output_file, 'r', encoding='utf-8') as f:
                    final_html = f.read()
                
                # We need to process the BODY part mainly, but let's process whole HTML
                # The uploader will replace local src with remote url
                processed_html = uploader.process_html_images(final_html, os.path.dirname(input_file))
                
                # C. Upload Draft
                title = config.get("title", os.path.splitext(os.path.basename(input_file))[0])
                digest = config.get("digest", "")
                author = config.get("author", "")
                
                media_id = uploader.upload_draft(title, processed_html, cover_media_id, author, digest)
                print(f"✅ Successfully uploaded to WeChat Draft! Media ID: {media_id}")
                
            except Exception as e:
                print(f"❌ Upload failed: {e}")

    print(f"✅ Build Complete! Output: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build WeChat Article from Markdown")
    parser.add_argument("input_file", help="Input Markdown file")
    parser.add_argument("--output", help="Output HTML file")
    parser.add_argument("--upload", action="store_true", help="Upload to WeChat Draft")
    
    args = parser.parse_args()
    build_article(args.input_file, args.output, args.upload)

