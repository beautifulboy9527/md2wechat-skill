import sys
import os
import json
import time
import requests
import subprocess
from PIL import Image
from io import BytesIO

def generate_image(prompt, binary_path):
    base_url = 'https://api-inference.modelscope.cn/'
    # Use env var
    api_key = os.getenv("IMAGE_API_KEY")
    if not api_key:
        print(json.dumps({"success": False, "error": "IMAGE_API_KEY environment variable is not set"}))
        sys.exit(1)

    common_headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    # 1. Generate Image
    try:
        response = requests.post(
            f"{base_url}v1/images/generations",
            headers={**common_headers, "X-ModelScope-Async-Mode": "true"},
            data=json.dumps({
                "model": "Tongyi-MAI/Z-Image-Turbo",
                "prompt": prompt
            }, ensure_ascii=False).encode('utf-8')
        )
        response.raise_for_status()
        task_id = response.json().get("task_id")
        if not task_id:
             raise Exception("No task_id returned")
    except Exception as e:
        print(json.dumps({"success": False, "error": f"Failed to start generation: {str(e)}"}))
        sys.exit(1)

    # 2. Poll for result
    image_url = None
    for _ in range(30): # 30 * 2s = 60s timeout
        try:
            result = requests.get(
                f"{base_url}v1/tasks/{task_id}",
                headers={**common_headers, "X-ModelScope-Task-Type": "image_generation"},
            )
            result.raise_for_status()
            data = result.json()

            if data["task_status"] == "SUCCEED":
                if "output_images" in data and len(data["output_images"]) > 0:
                    image_url = data["output_images"][0]
                    break
            elif data["task_status"] == "FAILED":
                print(json.dumps({"success": False, "error": f"Generation failed: {data.get('message', 'Unknown error')}"}))
                sys.exit(1)
        except Exception as e:
             print(json.dumps({"success": False, "error": f"Polling error: {str(e)}"}))
             sys.exit(1)
        
        time.sleep(2)
    
    if not image_url:
        print(json.dumps({"success": False, "error": "Generation timed out"}))
        sys.exit(1)

    # 3. Download Image
    temp_file = f"temp_{int(time.time())}.jpg"
    try:
        img_resp = requests.get(image_url)
        img_resp.raise_for_status()
        image = Image.open(BytesIO(img_resp.content))
        image.save(temp_file)
    except Exception as e:
        print(json.dumps({"success": False, "error": f"Failed to download/save image: {str(e)}"}))
        sys.exit(1)

    # 4. Upload using binary
    try:
        # We need to capture stdout
        # Ensure binary_path is absolute or correct relative
        cmd = [binary_path, "upload_image", temp_file]
        result = subprocess.check_output(cmd, stderr=subprocess.PIPE)
        upload_data = json.loads(result)
        
        if not upload_data.get("success"):
             print(result.decode('utf-8')) # Print the error from binary
             if os.path.exists(temp_file):
                os.remove(temp_file)
             sys.exit(1)
             
        # 5. Construct final response
        final_data = upload_data["data"]
        final_data["prompt"] = prompt
        final_data["original_url"] = image_url
        
        print(json.dumps({"success": True, "data": final_data}))
        
    except subprocess.CalledProcessError as e:
        print(json.dumps({"success": False, "error": f"Upload failed: {e.stderr.decode('utf-8')}"}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"success": False, "error": f"Processing error: {str(e)}"}))
        sys.exit(1)
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({"success": False, "error": "Usage: python generate_image.py <prompt> <binary_path>"}))
        sys.exit(1)
    
    prompt = sys.argv[1]
    binary_path = sys.argv[2]
    generate_image(prompt, binary_path)
