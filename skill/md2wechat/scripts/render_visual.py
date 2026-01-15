import argparse
import os
import sys
from jinja2 import Template
import style_prompts
import asyncio
# Import the async function from html_to_image.py. 
# Since it's in the same directory, we can import it directly if we run from there, 
# or append path.
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from html_to_image import html_to_image

def render_visual(type, content, style, output, title="Card"):
    # 1. Generate HTML Content
    html_content = ""
    
    if type == "html":
        # Use Jinja2 to fill template
        template_str = style_prompts.get_html_template(style)
        template = Template(template_str)
        html_content = template.render(title=title, content=content)
        
    elif type == "mermaid":
        # Wrap mermaid code in HTML template
        template_str = style_prompts.get_html_template("mermaid")
        template = Template(template_str)
        html_content = template.render(content=content)
        
    elif type == "svg":
        # If content is SVG code, wrap it in a simple HTML
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <body style="margin:0;padding:0;display:flex;justify-content:center;align-items:center;height:100vh;background:white;">
            {content}
        </body>
        </html>
        """
    else:
        print(f"Unknown type: {type}")
        sys.exit(1)

    # 2. Save HTML to temp file (optional, for debugging) or pass directly
    # For now, let's pass directly to html_to_image
    
    # 3. Render to Image
    try:
        asyncio.run(html_to_image(html_content, output))
        print(f"Successfully rendered {type} to {output}")
    except Exception as e:
        print(f"Error rendering: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Render visuals (HTML, Mermaid, SVG) to Image")
    parser.add_argument("type", choices=["html", "mermaid", "svg"], help="Type of visual")
    parser.add_argument("content", help="Content string or file path")
    parser.add_argument("output", help="Output image path")
    parser.add_argument("--style", default="apple", help="Style template for HTML")
    parser.add_argument("--title", default="Card", help="Title for HTML card")

    args = parser.parse_args()

    # Read content if it's a file
    content_val = args.content
    if os.path.exists(content_val):
        with open(content_val, 'r', encoding='utf-8') as f:
            content_val = f.read()

    render_visual(args.type, content_val, args.style, args.output, args.title)
