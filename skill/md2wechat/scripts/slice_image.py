from PIL import Image
import os
import sys

def slice_long_image(image_path, output_dir, max_height=2000):
    """
    Slices a long image into multiple shorter images.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    img = Image.open(image_path)
    width, height = img.size
    
    # If image is shorter than max_height, just copy it
    if height <= max_height:
        output_path = os.path.join(output_dir, "slice_0.jpg")
        img.save(output_path, quality=95)
        return [output_path]

    slices = []
    current_y = 0
    idx = 0
    
    while current_y < height:
        # Calculate slice height
        slice_h = min(max_height, height - current_y)
        
        # Crop
        box = (0, current_y, width, current_y + slice_h)
        slice_img = img.crop(box)
        
        # Save
        slice_filename = f"slice_{idx}.jpg"
        slice_path = os.path.join(output_dir, slice_filename)
        slice_img.save(slice_path, quality=95)
        slices.append(slice_path)
        
        current_y += slice_h
        idx += 1
        
    return slices

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python slice_image.py <input_image> <output_dir>")
        sys.exit(1)
        
    slice_long_image(sys.argv[1], sys.argv[2])
