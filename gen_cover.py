import requests
import time
import json
import os
from PIL import Image
from io import BytesIO

# Read config from md2wechat.yaml
api_key = None
if os.path.exists("md2wechat.yaml"):
    with open("md2wechat.yaml", "r", encoding="utf-8") as f:
        for line in f:
            if "image_key:" in line:
                parts = line.split(":", 1)
                if len(parts) == 2:
                    api_key = parts[1].strip().strip('"').strip("'")
                    break

if not api_key:
    api_key = os.getenv("IMAGE_API_KEY")

if not api_key:
    print("Error: API Key not found")
    exit(1)

base_url = 'https://api-inference.modelscope.cn/'

common_headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}

print("Generating image...")
try:
    response = requests.post(
        f"{base_url}v1/images/generations",
        headers={**common_headers, "X-ModelScope-Async-Mode": "true"},
        data=json.dumps({
            "model": "Tongyi-MAI/Z-Image-Turbo",
            "prompt": "A futuristic digital publishing assistant robot, glowing blue and cyan neon lights, high tech, cyberpunk style, wide aspect ratio",
            "n": 1,
            "size": "1024x1024"
        }, ensure_ascii=False).encode('utf-8')
    )

    response.raise_for_status()
    task_id = response.json()["task_id"]
    print(f"Task ID: {task_id}")

    while True:
        result = requests.get(
            f"{base_url}v1/tasks/{task_id}",
            headers={**common_headers, "X-ModelScope-Task-Type": "image_generation"},
        )
        result.raise_for_status()
        data = result.json()

        status = data["task_status"]
        print(f"Status: {status}")

        if status == "SUCCEED":
            image_url = data["output_images"][0]
            print(f"Downloading from {image_url}")
            image = Image.open(BytesIO(requests.get(image_url).content))
            image.save("cover.jpg")
            print("Saved to cover.jpg")
            break
        elif status == "FAILED":
            print("Image Generation Failed.")
            break

        time.sleep(2)

except Exception as e:
    print(f"Error: {e}")
