import os
import re
import time
import json
import base64
import sys
from bs4 import BeautifulSoup

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from generate_image import generate_image_file
except ImportError:
    generate_image_file = None

try:
    from html_to_image import html_to_image
    import asyncio
except ImportError:
    html_to_image = None

class AssetProcessor:
    def __init__(self, base_dir="."):
        self.base_dir = base_dir
        self.assets_dir = os.path.join(base_dir, "assets", "generated")
        if not os.path.exists(self.assets_dir):
            os.makedirs(self.assets_dir)

    def process(self, html_content):
        """
        Scans HTML for special tags and generates local assets.
        Returns processed HTML with local file paths.
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        images = soup.find_all('img')
        
        for img in images:
            src = img.get('src')
            if not src:
                continue

            new_src = None
            
            if src.startswith('__generate:'):
                new_src = self._handle_ai_generation(src)
            elif src.startswith('__html_base64:'):
                new_src = self._handle_html_render(src)
            elif src.startswith('__dataviz:'):
                new_src = self._handle_dataviz(src)
            
            if new_src:
                img['src'] = new_src
                # Add a class to mark it as processed/generated
                classes = img.get('class', [])
                if 'generated-asset' not in classes:
                    classes.append('generated-asset')
                img['class'] = classes

        return str(soup)

    def _handle_ai_generation(self, tag):
        if not generate_image_file:
            print("⚠️ generate_image module not found. Skipping.")
            return None

        # Parse tag: __generate:prompt|size=16:9__
        content = tag[len('__generate:'):]
        if content.endswith('__'): content = content[:-2]
        
        prompt = content
        size = None
        
        if '|' in content:
            parts = content.split('|')
            prompt = parts[0]
            for part in parts[1:]:
                if part.startswith('size=') or part.startswith('ratio='):
                    size = part.split('=')[1]

        print(f"🎨 Generating AI Image: {prompt[:30]}... (Size: {size})")
        
        filename = f"gen_{int(time.time())}_{hash(prompt)}.jpg"
        output_path = os.path.join(self.assets_dir, filename)
        
        try:
            # Call generator
            generate_image_file(prompt, output_path, size=size)
            return output_path
        except Exception as e:
            print(f"❌ Generation failed: {e}")
            return None

    def _handle_html_render(self, tag):
        if not html_to_image:
            print("⚠️ html_to_image module not found. Skipping.")
            return None

        # Parse tag: __html_base64:encoded_string__
        encoded = tag[len('__html_base64:'):]
        if encoded.endswith('__'): encoded = encoded[:-2]
        
        try:
            html_content = base64.b64decode(encoded).decode('utf-8')
            
            filename = f"viz_{int(time.time())}_{hash(encoded[:20])}.png"
            output_path = os.path.join(self.assets_dir, filename)
            
            print(f"📊 Rendering HTML Visualization to {filename}...")
            
            # We need to run async function in sync context
            # Create a temporary HTML file for the renderer
            temp_html_path = os.path.join(self.assets_dir, f"temp_{filename}.html")
            
            # Wrap in basic HTML if needed, but usually the converter does this or the renderer handles it.
            # Let's ensure it has a body.
            full_html = f"<!DOCTYPE html><html><body style='margin:0;padding:0;background:transparent;'>{html_content}</body></html>"
            
            with open(temp_html_path, 'w', encoding='utf-8') as f:
                f.write(full_html)
                
            # Run playwright
            asyncio.run(html_to_image(temp_html_path, output_path, width=1080))
            
            # Cleanup temp html
            if os.path.exists(temp_html_path):
                os.remove(temp_html_path)
                
            return output_path
            
        except Exception as e:
            print(f"❌ HTML Rendering failed: {e}")
            return None

    def _handle_dataviz(self, tag):
        # Placeholder for Data Viz logic
        # format: __dataviz:base64_json_config__
        print("⚠️ DataViz not implemented yet.")
        return None

if __name__ == "__main__":
    # Test
    html = '<img src="__generate:A cute cat|size=1:1__">'
    processor = AssetProcessor()
    print(processor.process(html))
