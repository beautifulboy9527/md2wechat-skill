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
        Also handles AI generation syntax: src="__generate:prompt"
        Returns processed HTML.
        """
        # Lazy import to avoid circular dependency if any, and ensure path is correct
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
                
                prompt = src[len('__generate:'):]
                print(f"🎨 Generating AI image for prompt: {prompt}...")
                
                temp_file = f"temp_gen_{int(time.time())}_{hash(prompt)}.jpg"
                try:
                    # Generate local file
                    local_path, _ = generate_image_file(prompt, temp_file)
                    
                    # Upload to WeChat
                    print(f"📤 Uploading generated image...")
                    media_id, wechat_url = self.upload_image(local_path)
                    img['src'] = wechat_url
                    
                    # Cleanup
                    if os.path.exists(local_path):
                        os.remove(local_path)
                        
                except Exception as e:
                    print(f"⚠️ Failed to generate/upload AI image: {e}")
                    # Keep placeholder or maybe set to a broken image indicator?
                    # For now, keep as is so user sees the error in src
            
            elif not src.startswith('http'):
                # Local file
                local_path = os.path.join(base_dir, src)
                print(f"📤 Uploading image: {local_path}...")
                try:
                    media_id, wechat_url = self.upload_image(local_path)
                    img['src'] = wechat_url
                    # img['data-src'] = wechat_url # WeChat sometimes uses data-src
                except Exception as e:
                    print(f"⚠️ Failed to upload image {src}: {e}")
        
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
            "thumb_media_id": thumb_media_id if thumb_media_id else "",
            "need_open_comment": 0,
            "only_fans_can_comment": 0
        }
        
        payload = {"articles": [article]}
        
        # Ensure proper encoding for Chinese characters
        resp = requests.post(url, data=json.dumps(payload, ensure_ascii=False).encode('utf-8'))
        data = resp.json()
        
        if "media_id" in data:
            return data["media_id"]
        else:
            raise Exception(f"Failed to upload draft: {data}")
