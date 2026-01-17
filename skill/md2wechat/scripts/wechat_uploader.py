import requests
import json
import os
import re
import time
from bs4 import BeautifulSoup

class WeChatUploader:
    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret
        self.token = None

    def get_access_token(self):
        if self.token:
            return self.token
        
        url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={self.app_id}&secret={self.app_secret}"
        resp = requests.get(url)
        data = resp.json()
        
        if "access_token" in data:
            self.token = data["access_token"]
            return self.token
        else:
            raise Exception(f"Failed to get access token: {data}")

    def upload_image(self, image_path):
        token = self.get_access_token()
        url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image"
        
        if not os.path.exists(image_path):
            raise Exception(f"Image not found: {image_path}")
            
        with open(image_path, 'rb') as f:
            files = {'media': f}
            resp = requests.post(url, files=files)
            
        data = resp.json()
        if "media_id" in data:
            return data["media_id"], data["url"]
        else:
            raise Exception(f"Failed to upload image {image_path}: {data}")

    def process_html_images(self, html_content, base_dir="."):
        """
        Finds local images in HTML, uploads them to WeChat, and replaces src with WeChat URL.
        Also handles AI generation syntax: src="__generate:prompt|size=16:9"
        Returns processed HTML.
        """
        try:
            import sys
            sys.path.append(os.path.dirname(os.path.abspath(__file__)))
            from generate_image import generate_image_file
        except ImportError:
            generate_image_file = None
            print("⚠️ Warning: generate_image module not found. AI generation will be skipped.")

        soup = BeautifulSoup(html_content, 'html.parser')
        images = soup.find_all('img')
        
        for img in images:
            src = img.get('src')
            if not src:
                continue

            if src.startswith('__generate:'):
                # AI Generation
                if not generate_image_file:
                    print(f"⚠️ Skipping AI generation for {src}: Module not available")
                    continue
                
                # Parse prompt and optional parameters (e.g. "prompt|size=16:9")
                raw_prompt = src[len('__generate:'):]
                prompt = raw_prompt
                size = None
                
                if '|' in raw_prompt:
                    parts = raw_prompt.split('|')
                    prompt = parts[0]
                    for part in parts[1:]:
                        if part.startswith('size=') or part.startswith('ratio='):
                            size = part.split('=')[1]
                            # Normalize ratio to size string if needed
                            if size == "16:9":
                                pass # generate_image handles this
                            elif size == "1:1":
                                pass
                            elif size == "9:16":
                                pass

                print(f"🎨 Generating AI image for prompt: {prompt} (Size: {size})...")
                
                temp_file = f"temp_gen_{int(time.time())}_{hash(prompt)}.jpg"
                try:
                    # Generate local file with size parameter
                    local_path, _ = generate_image_file(prompt, temp_file, size=size)
                    
                    # Upload to WeChat
                    print(f"📤 Uploading generated image...")
                    media_id, wechat_url = self.upload_image(local_path)
                    img['src'] = wechat_url
                    
                    # Cleanup
                    if os.path.exists(local_path):
                        os.remove(local_path)
                        
                except Exception as e:
                    print(f"⚠️ Failed to generate/upload AI image: {e}")

            elif src.startswith('__html_base64:'):
                # HTML Screenshot
                import base64
                encoded = src[len('__html_base64:'):]
                # Remove trailing __ if present
                if encoded.endswith('__'): encoded = encoded[:-2]
                
                try:
                    html_content = base64.b64decode(encoded).decode('utf-8')
                    print(f"📊 Rendering HTML visualization...")
                    
                    # Save to temp html
                    temp_html = f"temp_viz_{int(time.time())}.html"
                    temp_img = f"temp_viz_{int(time.time())}.png"
                    
                    # Wrap in basic HTML
                    full_viz_html = f"<html><body style='margin:0;padding:0;'>{html_content}</body></html>"
                    with open(temp_html, 'w', encoding='utf-8') as f:
                        f.write(full_viz_html)
                        
                    # Render using html_to_image.py (subprocess)
                    import subprocess
                    script_dir = os.path.dirname(os.path.abspath(__file__))
                    render_script = os.path.join(script_dir, "html_to_image.py")
                    
                    subprocess.run(
                        ["python", render_script, temp_html, temp_img, "--width", "1080"],
                        check=True
                    )
                    
                    # Upload
                    print(f"📤 Uploading visualization...")
                    media_id, wechat_url = self.upload_image(temp_img)
                    img['src'] = wechat_url
                    
                    # Cleanup
                    if os.path.exists(temp_html): os.remove(temp_html)
                    if os.path.exists(temp_img): os.remove(temp_img)
                    
                except Exception as e:
                    print(f"⚠️ Failed to render/upload HTML viz: {e}")
            
            elif not src.startswith('http'):
                # Local file
                local_path = os.path.join(base_dir, src)
                print(f"📤 Uploading image: {local_path}...")
                try:
                    media_id, wechat_url = self.upload_image(local_path)
                    img['src'] = wechat_url
                except Exception as e:
                    print(f"⚠️ Failed to upload image {src}: {e}")
        
        # FINAL CLEANUP: Ensure we return only the body content (fragment)
        # If the soup contains <html> or <body> tags, extract the inner content.
        if soup.body:
            # Return the inner HTML of the body
            return "".join([str(x) for x in soup.body.contents])
        
        # If no body tag, but has html tag?
        if soup.html:
            return "".join([str(x) for x in soup.html.contents])
            
        return str(soup)

    def upload_draft(self, title, content, thumb_media_id=None, author="", digest=""):
        token = self.get_access_token()
        url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}"
        
        article = {
            "title": title,
            "author": author,
            "digest": digest,
            "content": content,
            "content_source_url": "",
            "need_open_comment": 0,
            "only_fans_can_comment": 0
        }
        
        if thumb_media_id:
            article["thumb_media_id"] = thumb_media_id
        
        payload = {"articles": [article]}
        
        resp = requests.post(url, data=json.dumps(payload, ensure_ascii=False).encode('utf-8'))
        data = resp.json()
        
        if "media_id" in data:
            return data["media_id"]
        else:
            raise Exception(f"Failed to upload draft: {data}")
