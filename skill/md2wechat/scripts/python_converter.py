import markdown
import yaml
import os
import css_inline
from bs4 import BeautifulSoup
import copy

def split_html_by_sections(html_content, card_mode=False):
    """
    Splits HTML content into sections based on H1/H2 headers.
    Returns a list of complete HTML strings (with head/styles) for each section.
    """

    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract head/styles to re-apply to each section
    head = soup.head
    if not head:
        head = soup.new_tag("head")
    
    # Find the container
    container = soup.find("div", class_="wechat-container")
    if not container:
        container = soup.body
        
    sections = []
    current_section = []
    
    # Helper to finalize a section
    def finalize_section(nodes):
        if not nodes:
            return
        
        new_soup = BeautifulSoup("<!DOCTYPE html><html></html>", 'html.parser')
        new_soup.html.append(copy.copy(head))
        
        if card_mode:
            # Card Mode: Gray background, centered card with shadow
            # Note: We removed 'background: #fff' and 'color: #333' to let the Theme CSS control it.
            new_body = new_soup.new_tag("body", attrs={"style": "margin: 0; padding: 20px; background-color: #f0f2f5;"})
            new_container = new_soup.new_tag("div", attrs={
                "class": "wechat-container",
                "style": "width: 85%; max-width: 800px; margin: 20px auto; padding: 50px; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 17px; line-height: 1.8;"
            })
        else:
            # Normal Mode: White background, full width
            new_body = new_soup.new_tag("body", attrs={"style": "margin: 0; padding: 0; background-color: #fff;"})
            new_container = new_soup.new_tag("div", attrs={
                "class": "wechat-container",
                "style": "padding: 20px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 17px; line-height: 1.6; color: #333;"
            })

        
        # Apply body styles to container if needed, or just rely on CSS
        # In our converter, we put styles in <head>, so just structure is enough.
        
        for node in nodes:
            new_container.append(node)
            
        new_body.append(new_container)
        new_soup.html.append(new_body)
        sections.append(str(new_soup))

    # Iterate through children
    for child in container.children:
        if child.name in ['h1', 'h2']:
            # If we have accumulated content, save it as a section
            if current_section:
                finalize_section(current_section)
                current_section = []
            # Start new section with this header
            current_section.append(copy.copy(child))
        else:
            # Append to current section
            if child.name or (isinstance(child, str) and child.strip()):
                 current_section.append(copy.copy(child))
                 
    # Final section
    if current_section:
        finalize_section(current_section)
        
    return sections


def load_theme(theme_name, themes_dir):
    # Try .yaml and .yml
    for ext in ['.yaml', '.yml']:
        path = os.path.join(themes_dir, f"{theme_name}{ext}")
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
    return None

def convert_markdown_to_wechat(markdown_content, theme_name="default", themes_dir="themes"):
    # 1. Load Theme
    theme = load_theme(theme_name, themes_dir)
    css = ""
    if theme and "prompt" in theme:
        # The YAML contains a "prompt" field which has the CSS inside it (for AI context).
        # We need to extract the CSS part. 
        # This is a bit hacky because the YAML structure was designed for LLM prompts, not direct parsing.
        # But let's try to extract the CSS block from the prompt string.
        prompt = theme["prompt"]
        import re
        css_match = re.search(r'/\*.*?\*/', prompt, re.DOTALL) # Find first comment? No.
        # Let's look for the block between "CSS 样式规则" and the end or "输出要求".
        # Or simpler: just extract everything that looks like CSS.
        # Actually, let's just use a regex to find the CSS block if possible, or maybe the user should provide a clean CSS file.
        # Given the current state, let's try to extract content between `/*` and `*/` and the rules.
        # A better approach for the future: Add a 'css' field to the YAML.
        # For now, let's try to parse the prompt text.
        
        # Strategy: Extract lines that look like CSS (selectors and braces).
        # Or better: The prompt says "请严格按照以下 CSS 样式规则...".
        # We can try to find the CSS code block in the prompt.
        pass

    # Fallback: If we can't easily parse CSS from the prompt text, let's use a default CSS or expect a 'style' field.
    # To make this robust, I will create a simple mapping or just use a basic style for now.
    # Wait, I can read the YAML file again.
    # Let's look at `chinese-scroll.yaml`. It has CSS inside the `prompt` string.
    # It's mixed with text.
    
    # Let's try a smarter extraction:
    # Find the start of the CSS block. Usually starts with `/*`.
    # Find the end.
    if theme:
        prompt = theme.get("prompt", "")
        start_marker = "/*"
        end_marker = "输出要求"
        start_idx = prompt.find(start_marker)
        end_idx = prompt.find(end_marker)
        
        if start_idx != -1:
            if end_idx != -1:
                css = prompt[start_idx:end_idx]
            else:
                css = prompt[start_idx:]
    
    # 2. Convert Markdown to HTML
    html_body = markdown.markdown(markdown_content, extensions=['fenced_code', 'tables', 'nl2br'])
    
    # 3. Wrap in Container
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head><style>{css}</style></head>
    <body>
        <div class="wechat-container">
            {html_body}
        </div>
    </body>
    </html>
    """
    
    # 4. Inline CSS
    inlined_html = css_inline.inline(full_html)
    
    # 5. Extract body content (WeChat doesn't want full HTML doc usually, just the body parts)
    # But for preview/file saving, full HTML is fine.
    # For copy-paste, we usually want what's inside body.
    soup = BeautifulSoup(inlined_html, 'html.parser')
    body_content = soup.body.decode_contents()
    
    return body_content

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python python_converter.py <input_md> [theme]")
        sys.exit(1)
        
    input_file = sys.argv[1]
    theme = sys.argv[2] if len(sys.argv) > 2 else "default"
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    html = convert_markdown_to_wechat(content, theme, os.path.join(os.path.dirname(__file__), "../../themes"))
    print(html)
