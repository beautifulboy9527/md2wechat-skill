import asyncio
import argparse
import os
import sys
from playwright.async_api import async_playwright

async def html_to_image(input_path, output_path, width=1000, height=None, selector=None):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': width, 'height': height or 800})
        
        # Handle local file or raw HTML string
        if os.path.exists(input_path):
            url = f'file://{os.path.abspath(input_path)}'
            await page.goto(url)
        else:
            # Assume input_path is raw HTML content if file doesn't exist
            await page.set_content(input_path)

        # Wait for network idle to ensure assets load
        await page.wait_for_load_state('networkidle')

        # Locate element to screenshot
        if selector:
            element = await page.query_selector(selector)
            if element:
                await element.screenshot(path=output_path)
            else:
                print(f"Error: Selector '{selector}' not found.")
                await browser.close()
                return False
        else:
            # Full page screenshot
            await page.screenshot(path=output_path, full_page=True)

        await browser.close()
        return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert HTML to Image using Playwright")
    parser.add_argument("input", help="Input HTML file path or content")
    parser.add_argument("output", help="Output image path")
    parser.add_argument("--width", type=int, default=1080, help="Viewport width")
    parser.add_argument("--height", type=int, default=800, help="Viewport height")
    parser.add_argument("--selector", help="CSS selector to screenshot")

    args = parser.parse_args()

    # If input is a file that doesn't exist, treat it as content? 
    # Actually, let's be strict. If it looks like a path but doesn't exist, warn.
    # But for flexibility, we'll assume if it starts with < it's HTML.
    
    input_val = args.input
    if not os.path.exists(input_val) and not input_val.strip().startswith("<"):
         # Try to read from stdin if input is "-"
         if input_val == "-":
             input_val = sys.stdin.read()
    
    try:
        asyncio.run(html_to_image(input_val, args.output, args.width, args.height, args.selector))
        print(f"Successfully saved to {args.output}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
