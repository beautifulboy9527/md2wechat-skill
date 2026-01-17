import sys
import os
import json
import time
import requests
from PIL import Image
from io import BytesIO

# Add current directory to path to import style_prompts
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    import style_prompts
except ImportError:
    style_prompts = None

def generate_image_file(prompt, output_path, style=None, sub_style=None, size=None):
    """
    Generates an image using ModelScope API (Wanx-v1 for better ratio control).
    """
    # Enhance prompt
    if style and style_prompts:
        suffix = style_prompts.get_style_prompt(style, sub_style)
        if suffix:
            prompt += suffix

    # Add ratio keywords
    if size == "16:9":
        prompt += ", wide angle, 16:9 aspect ratio, cinematic composition, high resolution, 4k"
    
    base_url = 'https://api-inference.modelscope.cn/'
    api_key = os.getenv("IMAGE_API_KEY")
    
    if not api_key:
        # Try to read from md2wechat.yaml
        config_files = ["md2wechat.yaml", "md2wechat.yml", ".md2wechat.yaml", ".md2wechat.yml"]
        for config_file in config_files:
            if os.path.exists(config_file):
                try:
                    with open(config_file, 'r', encoding='utf-8') as f:
                        for line in f:
                            if "image_key:" in line:
                                parts = line.split(":", 1)
                                if len(parts) == 2:
                                    key_val = parts[1].strip().strip('"').strip("'")
                                    if key_val:
                                        api_key = key_val
                                        break
                except Exception:
                    pass
            if api_key:
                break

    if not api_key:
        raise Exception("IMAGE_API_KEY not set")

    common_headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "X-ModelScope-Async-Mode": "true"
    }

    # Use Z-Image-Turbo
    model_id = "Tongyi-MAI/Z-Image-Turbo"
    
    # Determine size
    img_size = "1024x1024"
    if size == "16:9":
        img_size = "2048x1152" 
        
    # OpenAI-compatible format (mostly)
    payload = {
        "model": model_id,
        "prompt": prompt,
        "size": img_size,
        "n": 1
    }

    print(f"🎨 Generating image with {model_id} (Size: {img_size})...")

    try:
        # Use the v1/images/generations endpoint
        response = requests.post(
            f"{base_url}v1/images/generations",
            headers={**common_headers, "X-ModelScope-Async-Mode": "true"},
            data=json.dumps(payload, ensure_ascii=False).encode('utf-8')
        )
        response.raise_for_status()
        task_id = response.json().get("task_id")
    except Exception as e:
        print(f"⚠️ Generation request failed: {e}")
        # Print response content if available for debugging
        if 'response' in locals():
            print(f"Response: {response.text}")
        raise

    # Poll
    image_url = None
    for _ in range(60):
        try:
            result = requests.get(
                f"{base_url}v1/tasks/{task_id}",
                headers={**common_headers, "X-ModelScope-Task-Type": "image_generation"},
            )
            data = result.json()
            if data["task_status"] == "SUCCEED":
                # Z-Image-Turbo returns output_images list
                if "output_images" in data and data["output_images"]:
                    image_url = data["output_images"][0]
                # Fallback
                elif "results" in data.get("output", {}):
                     image_url = data["output"]["results"][0]["url"]
                break
            elif data["task_status"] == "FAILED":
                raise Exception(f"Generation failed: {data.get('message')}")
        except Exception:
            pass
        time.sleep(2)
    
    if not image_url:
        raise Exception("Timeout")

    # Download
    img_resp = requests.get(image_url)
    image = Image.open(BytesIO(img_resp.content))
    
    # No cropping needed as Z-Image-Turbo supports native ratio
    image.save(output_path)
    return output_path, image_url

if __name__ == "__main__":
    if len(sys.argv) < 3: sys.exit(1)
    generate_image_file(sys.argv[1], sys.argv[2], 
                       sys.argv[3] if len(sys.argv)>3 else None,
                       sys.argv[4] if len(sys.argv)>4 else None,
                       sys.argv[5] if len(sys.argv)>5 else None)
