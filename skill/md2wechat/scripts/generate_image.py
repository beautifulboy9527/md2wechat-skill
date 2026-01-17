import sys
import os
import json
import time
import requests
import yaml
from PIL import Image
from io import BytesIO

# Add current directory to path to import style_prompts
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    import style_prompts
except ImportError:
    style_prompts = None

def load_config():
    """Load configuration from md2wechat.yaml"""
    config_files = ["md2wechat.yaml", "md2wechat.yml", ".md2wechat.yaml", ".md2wechat.yml"]
    
    # Check current directory
    for f in config_files:
        if os.path.exists(f):
            try:
                with open(f, 'r', encoding='utf-8') as file:
                    return yaml.safe_load(file) or {}
            except Exception as e:
                print(f"⚠️ Error loading config {f}: {e}")
    
    # Check home directory
    home_dir = os.path.expanduser("~")
    for f in config_files:
        path = os.path.join(home_dir, f)
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as file:
                    return yaml.safe_load(file) or {}
            except Exception:
                pass
                
    return {}

def generate_image_openai(prompt, output_path, config, size=None):
    """
    Generic OpenAI-compatible image generation.
    Supports DALL-E 3, Flux, Midjourney-API, etc.
    """
    api_key = config.get("image_key") or os.getenv("IMAGE_API_KEY")
    base_url = config.get("image_api_base", "https://api.openai.com/v1")
    model = config.get("image_model", "dall-e-3")
    
    if not api_key:
        raise Exception("Missing API Key. Please set 'image_key' in md2wechat.yaml or IMAGE_API_KEY env var.")

    # Normalize Base URL
    if not base_url.endswith("/"):
        base_url += "/"
    
    # If user provided a full path (e.g. .../generations), use it. 
    # Otherwise append v1/images/generations standard.
    if "generations" not in base_url:
        endpoint = f"{base_url}images/generations"
    else:
        endpoint = base_url

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Size mapping
    img_size = "1024x1024"
    if size == "16:9":
        img_size = "1024x1024" # DALL-E 3 standard, usually 1024x1792 or similar. 
        # Many 3rd party APIs expect specific strings.
        # Let's try to be smart or allow user override.
        if "dall-e-3" in model:
            img_size = "1792x1024" # Landscape
        else:
            img_size = "1024x1024" # Safe default

    payload = {
        "model": model,
        "prompt": prompt,
        "size": img_size,
        "n": 1
    }

    print(f"🎨 Generating with {model} via {endpoint}...")
    
    try:
        response = requests.post(endpoint, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        
        # Standard OpenAI response: {"data": [{"url": "..."}]}
        if "data" in data and len(data["data"]) > 0:
            image_url = data["data"][0]["url"]
        else:
            raise Exception(f"Unexpected response format: {data}")
            
    except Exception as e:
        print(f"❌ OpenAI Generation failed: {e}")
        if 'response' in locals():
            print(f"Response: {response.text}")
        raise

    # Download and Save
    print(f"⬇️ Downloading image...")
    img_resp = requests.get(image_url)
    image = Image.open(BytesIO(img_resp.content))
    image.save(output_path)
    return output_path, image_url

def generate_image_modelscope(prompt, output_path, config, size=None):
    """
    Legacy ModelScope (Wanx/Tongyi) generation with async polling.
    """
    api_key = config.get("image_key") or os.getenv("IMAGE_API_KEY")
    base_url = 'https://api-inference.modelscope.cn/'
    
    if not api_key:
        raise Exception("IMAGE_API_KEY not set")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "X-ModelScope-Async-Mode": "true"
    }

    model_id = config.get("image_model", "Tongyi-MAI/Z-Image-Turbo")
    
    # Determine size
    img_size = "1024x1024"
    if size == "16:9":
        img_size = "2048x1152" 
        
    payload = {
        "model": model_id,
        "prompt": prompt,
        "size": img_size,
        "n": 1
    }

    print(f"🎨 Generating with ModelScope {model_id}...")

    # 1. Submit Task
    response = requests.post(
        f"{base_url}v1/images/generations",
        headers=headers,
        json=payload
    )
    response.raise_for_status()
    task_id = response.json().get("task_id")

    # 2. Poll Status
    image_url = None
    for _ in range(60):
        try:
            result = requests.get(
                f"{base_url}v1/tasks/{task_id}",
                headers={**headers, "X-ModelScope-Task-Type": "image_generation"},
            )
            data = result.json()
            if data["task_status"] == "SUCCEED":
                if "output_images" in data and data["output_images"]:
                    image_url = data["output_images"][0]
                elif "results" in data.get("output", {}):
                     image_url = data["output"]["results"][0]["url"]
                break
            elif data["task_status"] == "FAILED":
                raise Exception(f"Task Failed: {data.get('message')}")
        except Exception:
            pass
        time.sleep(2)
    
    if not image_url:
        raise Exception("Timeout waiting for image")

    # 3. Download
    img_resp = requests.get(image_url)
    image = Image.open(BytesIO(img_resp.content))
    image.save(output_path)
    return output_path, image_url

def generate_image_file(prompt, output_path, style=None, sub_style=None, size=None):
    # Load Config
    config = load_config()
    
    # Enhance prompt
    if style and style_prompts:
        suffix = style_prompts.get_style_prompt(style, sub_style)
        if suffix:
            prompt += suffix

    # Add ratio keywords if needed
    if size == "16:9":
        prompt += ", wide angle, 16:9 aspect ratio, cinematic composition"

    # Determine Provider
    # Default to 'modelscope' for backward compatibility if not specified
    provider = config.get("image_provider", "modelscope")
    
    try:
        if provider == "openai":
            return generate_image_openai(prompt, output_path, config, size)
        else:
            # Default to ModelScope
            return generate_image_modelscope(prompt, output_path, config, size)
    except Exception as e:
        print(f"⚠️ Image generation failed: {e}")
        raise

if __name__ == "__main__":
    if len(sys.argv) < 3: sys.exit(1)
    generate_image_file(sys.argv[1], sys.argv[2], 
                       sys.argv[3] if len(sys.argv)>3 else None,
                       sys.argv[4] if len(sys.argv)>4 else None,
                       sys.argv[5] if len(sys.argv)>5 else None)
