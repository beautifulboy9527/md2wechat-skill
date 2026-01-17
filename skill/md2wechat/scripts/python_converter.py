import markdown
import yaml
import os
import css_inline
from bs4 import BeautifulSoup
import copy
import re

def strip_frontmatter(content):
    """
    Removes YAML frontmatter from markdown content.
    Returns (cleaned_content, frontmatter_dict)
    """
    frontmatter = {}
    if content.startswith("---"):
        try:
            # Find the second "---"
            parts = content.split("---", 2)
            if len(parts) >= 3:
                yaml_text = parts[1]
                frontmatter = yaml.safe_load(yaml_text)
                content = parts[2].strip()
        except Exception as e:
            print(f"⚠️ Error parsing frontmatter: {e}")
            
    return content, frontmatter

def load_theme(theme_name, themes_dir):
    # Try .yaml and .yml
    for ext in ['.yaml', '.yml']:
        path = os.path.join(themes_dir, f"{theme_name}{ext}")
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f)
            except Exception as e:
                print(f"⚠️ Failed to load theme {path}: {e}")
    return None

def convert_markdown_to_wechat(markdown_content, theme_name="default", themes_dir="themes"):
    # 1. Strip Frontmatter FIRST
    markdown_content, frontmatter = strip_frontmatter(markdown_content)
    
    # 2. Load Theme
    # Priority: Theme from arg > Theme from frontmatter > Default
    if not theme_name or theme_name == "default":
        theme_name = frontmatter.get("theme", "ocean-calm")
        
    theme = load_theme(theme_name, themes_dir)
    css = ""
    
    if theme:
        # Strategy A: Structured Fields (like ocean-calm.yaml)
        # IMPORTANT: We use simple selectors (element names) because css_inline works best with them.
        # We also add .wechat-container prefix for specificity if needed, but for inline it's better to be direct.
        
        style_parts = []
        # Global container style
        if theme.get("container_style"): 
            if theme.get("use_table_wrapper"):
                style_parts.append(f".main-container {{ {theme['container_style']} }}")
            else:
                style_parts.append(f"body {{ {theme['container_style']} }}")
            
        # Element styles - Apply directly to elements
        if theme.get("h1_style"): style_parts.append(f"h1 {{ {theme['h1_style']} }}")
        if theme.get("h2_style"): style_parts.append(f"h2 {{ {theme['h2_style']} }}")
        if theme.get("h3_style"): style_parts.append(f"h3 {{ {theme['h3_style']} }}")
        if theme.get("h4_style"): style_parts.append(f"h4 {{ {theme['h4_style']} }}")
        if theme.get("p_style"): style_parts.append(f"p {{ {theme['p_style']} }}")
        if theme.get("strong_style"): style_parts.append(f"strong {{ {theme['strong_style']} }}")
        if theme.get("blockquote_style"): style_parts.append(f"blockquote {{ {theme['blockquote_style']} }}")
        if theme.get("ul_style"): style_parts.append(f"ul {{ {theme['ul_style']} }}")
        if theme.get("ol_style"): style_parts.append(f"ol {{ {theme['ol_style']} }}")
        if theme.get("li_style"): style_parts.append(f"li {{ {theme['li_style']} }}")
        
        # Code blocks
        if theme.get("pre_style"): style_parts.append(f"pre {{ {theme['pre_style']} }}")
        if theme.get("code_style"): style_parts.append(f"code {{ {theme['code_style']} }}")
        
        if theme.get("image_style"): style_parts.append(f"img {{ {theme['image_style']} }}")
        if theme.get("link_style"): style_parts.append(f"a {{ {theme['link_style']} }}")
        if theme.get("hr_style"): style_parts.append(f"hr {{ {theme['hr_style']} }}")
        
        # Support for extra/custom CSS
        if theme.get("extra_css"):
            style_parts.append(theme["extra_css"])
        
        if style_parts:
            css = "\n".join(style_parts)
            print(f"   ℹ️ Constructed CSS from structured fields ({len(style_parts)} rules)")
            
        # Strategy B: Embedded CSS in 'prompt'
        elif "prompt" in theme:
            prompt = theme["prompt"]
            start_marker = "/*"
            end_marker = "输出要求"
            
            start_idx = prompt.find(start_marker)
            if start_idx != -1:
                end_idx = prompt.find(end_marker, start_idx)
                if end_idx != -1:
                    css = prompt[start_idx:end_idx]
                else:
                    css = prompt[start_idx:]
                print("   ℹ️ Extracted CSS from 'prompt' field")
    
    if not css:
        print("   ⚠️ No CSS found, using defaults.")
        css = "body { font-family: sans-serif; } img { max-width: 100%; }"

    # 3. Convert Markdown to HTML
    # Use 'extra' for better features, 'codehilite' for code blocks
    html_body = markdown.markdown(
        markdown_content, 
        extensions=[
            'fenced_code', 
            'tables', 
            'nl2br', 
            'attr_list', 
            'sane_lists'
        ]
    )
    
    # --- SMART IMAGE INSERTION LOGIC ---
    # If auto_image is enabled in frontmatter, insert image placeholders after H2
    if frontmatter.get("auto_image", False):
        soup = BeautifulSoup(html_body, 'html.parser')
        h2_tags = soup.find_all('h2')
        for i, h2 in enumerate(h2_tags):
            # Create image placeholder
            # Use the H2 text as the prompt context
            prompt_text = h2.get_text().strip()
            if prompt_text:
                img_placeholder = soup.new_tag('img')
                # Add size=16:9 to the generate tag
                img_placeholder['src'] = f"__generate:{prompt_text}|size=16:9__"
                img_placeholder['alt'] = f"Illustration for {prompt_text}"
                img_placeholder['class'] = "auto-generated-image"
                # Insert after the H2
                h2.insert_after(img_placeholder)
        html_body = str(soup)
        print(f"   ✨ Auto-inserted {len(h2_tags)} image placeholders after H2 tags.")

    # --- THEME WRAPPER LOGIC ---
    # Some themes (like dark mode) need a Table wrapper to preserve background color on WeChat.
    if theme:
        if theme.get("wrapper"):
            # Custom wrapper with {{content}} placeholder
            html_body = theme["wrapper"].replace("{{content}}", html_body)
            print("   ✨ Applied custom theme wrapper.")
        elif theme.get("use_table_wrapper", False):
            # Standard single-cell table wrapper for WeChat stability
            # We add a class 'main-container' to the TD so CSS can target it.
            html_body = f"""
            <table width="100%" cellspacing="0" cellpadding="0" border="0">
                <tr>
                    <td class="main-container">
                        {html_body}
                    </td>
                </tr>
            </table>
            """
            print("   ✨ Applied standard table wrapper for WeChat stability.")

    # --- LIST FLATTENING LOGIC (Fix for WeChat) ---
    # Helper function to flatten lists
    def flatten_lists(soup_obj):
        try:
            # Define a hanging indent style for list items
            list_item_style = "margin: 0 0 10px 0; padding-left: 32px; text-indent: -22px; line-height: 1.7;"
            
            # Process UL
            for ul in soup_obj.find_all('ul'):
                new_tags = []
                for li in ul.find_all('li', recursive=False):
                    # Unwrap <p> inside <li>
                    p_in_li = li.find('p')
                    if p_in_li:
                        p_in_li.unwrap()
                    
                    # Create new P
                    p = soup_obj.new_tag('p')
                    p['style'] = list_item_style
                    # Add bullet
                    p.string = f"•  {li.get_text().strip()}"
                    new_tags.append(p)
                
                # Replace UL with new Ps
                for tag in reversed(new_tags):
                    ul.insert_after(tag)
                ul.decompose()

            # Process OL
            for ol in soup_obj.find_all('ol'):
                new_tags = []
                for i, li in enumerate(ol.find_all('li', recursive=False)):
                    # Unwrap <p> inside <li>
                    p_in_li = li.find('p')
                    if p_in_li:
                        p_in_li.unwrap()
                    
                    # Create new P
                    p = soup_obj.new_tag('p')
                    p['style'] = list_item_style
                    # Add number
                    p.string = f"{i+1}. {li.get_text().strip()}"
                    new_tags.append(p)
                
                # Replace OL with new Ps
                for tag in reversed(new_tags):
                    ol.insert_after(tag)
                ol.decompose()
        except Exception as e:
            print(f"   ⚠️ List flattening failed: {e}")

    # Apply flattening to main body
    try:
        soup = BeautifulSoup(html_body, 'html.parser')
        flatten_lists(soup)
        html_body = str(soup)
        print("   ✨ Flattened lists to paragraphs for better WeChat compatibility.")
    except Exception as e:
        print(f"   ⚠️ Main list flattening failed: {e}")

    # --- HTML SCREENSHOT LOGIC ---
    # Detect code blocks marked as 'viz', 'html-render', or 'mermaid' and convert to screenshot placeholder
    # Syntax: ```viz ... ```
    # Or inline: ![chart](__html:<div>...</div>__)
    
    # 1. Handle Inline __html: syntax
    # Already handled by wechat_uploader if we use a specific prefix? 
    # Actually, wechat_uploader handles __generate:. We need a similar handler for __html:.
    # But for now, let's just ensure the src attribute is preserved for the uploader to handle.
    # The markdown parser will turn ![chart](__html:...) into <img src="__html:..."> which is fine.
    
    # 2. Handle Code Blocks
    # We need to find <pre><code class="language-viz">...</code></pre>
    # Note: 'fenced_code' extension might not add class if not configured, or adds 'language-viz'.
    # Let's check for 'viz' or 'html' class.
    soup = BeautifulSoup(html_body, 'html.parser')
    code_blocks = soup.find_all('code')
    for code in code_blocks:
        classes = code.get('class', [])
        # Added 'language-mermaid' support
        if 'language-viz' in classes or 'language-html-render' in classes or 'language-mermaid' in classes:
            # This is a block we want to render as image
            content = code.get_text()
            
            # For mermaid, we might need to wrap it in a div with class mermaid for the renderer?
            # The html_to_image.py script needs to handle it.
            # For now, let's assume the renderer can handle raw mermaid code if we wrap it or if we pass a flag.
            # But our current uploader logic just dumps the content into a body.
            # If it's mermaid, we should probably wrap it in <div class="mermaid">...</div> and ensure the renderer has mermaid.js.
            # This is a bit complex for a quick fix.
            # ALTERNATIVE: Just treat it as a code block for now if we can't render it easily.
            # But the user specifically asked for "配图 logic".
            # Let's try to render it. We'll wrap it in a specific structure.
            
            if 'language-mermaid' in classes:
                # Wrap in a way that html_to_image.py (if updated) or a simple html template can render.
                # We'll use a special prefix __mermaid_base64: maybe?
                # Or just stick to __html_base64: and wrap it in a script tag?
                # Let's wrap it in a div that loads mermaid via CDN.
                mermaid_html = f"""
                <div class="mermaid">
                {content}
                </div>
                <script type="module">
                import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
                mermaid.initialize({{ startOnLoad: true }});
                </script>
                """
                import base64
                encoded = base64.b64encode(mermaid_html.encode('utf-8')).decode('utf-8')
                img = soup.new_tag('img')
                img['src'] = f"__html_base64:{encoded}__"
                img['alt'] = "Mermaid Diagram"
                img['class'] = "mermaid-viz-image"
                
            else:
                # Standard HTML viz
                import base64
                encoded = base64.b64encode(content.encode('utf-8')).decode('utf-8')
                img = soup.new_tag('img')
                img['src'] = f"__html_base64:{encoded}__" 
                img['alt'] = "HTML Visualization"
                img['class'] = "html-viz-image"
            
            # Replace the pre tag (parent) with this img
            if code.parent.name == 'pre':
                code.parent.replace_with(img)
    
    html_body = str(soup)

    # --- PROMPT BLOCK STYLING ---
    # Detect code blocks that look like prompts and style them as cards.
    # Also format the text to ensure "one rule per line" for better readability.
    soup = BeautifulSoup(html_body, 'html.parser')
    pre_tags = soup.find_all('pre')
    for pre in pre_tags:
        code = pre.find('code')
        if code:
            text = code.get_text()
            # Heuristic: If it looks like a prompt or user explicitly marked it
            if "Prompt:" in text or "提示词:" in text or "ContentAny" in text: 
                print(f"   ✨ Detected Prompt Card. Length: {len(text)}")
                
                # Strategy: "Table-wrapped Hard Break Markdown"
                # WeChat sometimes strips styles from <div> or <pre>.
                # A single-cell <table> is the most robust way to preserve background and borders.
                
                print("   ℹ️ Strategy: Wrapping Prompt Card in a Table for WeChat stability...")

                # 0. Clean up "markdown" fence leakage
                lines = text.split('\n')
                cleaned_lines = []
                for line in lines:
                    stripped = line.strip()
                    if stripped.startswith('```') or stripped == 'markdown':
                        continue
                    cleaned_lines.append(line)
                text = '\n'.join(cleaned_lines)

                # 1. Escape HTML special characters
                import html
                text = html.escape(text)

                # 2. De-clump and Convert Newlines to <br>
                
                # Headers: " ##" -> "<br><br>##"
                text = re.sub(r'[ \t](#{1,})', r'<br><br>\1', text)
                
                # Numbered items: " 1." -> "<br>1."
                text = re.sub(r'[ \t](\d+\.)[ \t]', r'<br>\1 ', text)
                
                # Specific Fix: " - **" (Bullet followed by bold) -> Just break, no bullet
                # This fixes the "extra -" issue for Key-Value pairs
                text = re.sub(r'[ \t][-][ \t](\*\*)', r'<br>\1', text)
                
                # Standard Bullets: " - " -> "<br>- "
                text = re.sub(r'[ \t]([-*])[ \t]', r'<br>\1 ', text)
                
                # Chinese Numbers: " 1、" -> "<br>1、"
                text = re.sub(r'[ \t](\d+、)', r'<br>\1', text)
                
                # Key-Value pairs: "**Key**: Value" (if not caught by above)
                text = re.sub(r'[ \t](\*\*.+?\*\*)', r'<br>\1', text)
                
                # Specific fix for the known template structure
                text = text.replace("] 2.", "]<br>2.")
                text = text.replace("] 3.", "]<br>3.")
                text = text.replace("] 4.", "]<br>4.")
                text = text.replace("] 5.", "]<br>5.")

                # Convert original newlines to <br>
                text = text.replace('\n', '<br>')
                
                # 3. Post-processing Cleanup
                # Split by <br>, remove empty/lone-hyphen segments, rejoin
                segments = text.split('<br>')
                final_segments = []
                for seg in segments:
                    s = seg.strip()
                    # Remove lone hyphens, bullets, or empty lines
                    if s in ['-', '*', '']:
                        continue
                    final_segments.append(seg)
                text = '<br>'.join(final_segments)
                
                # Clean up multiple <br>s (just in case)
                text = re.sub(r'(<br>){3,}', '<br><br>', text)
                
                # Remove leading <br>
                while text.startswith('<br>'):
                    text = text[4:]

                # 4. Create Table Structure
                # <table><tr><td> Content </td></tr></table>
                table = soup.new_tag('table')
                table['style'] = (
                    "width: 100%; "
                    "border-collapse: separate; " # separate needed for border-radius
                    "border-spacing: 0; "
                    "border: 1px solid #e1e4e8; "
                    "border-radius: 6px; "
                    "background-color: #f6f8fa; "
                    "margin: 20px 0;"
                )
                
                tr = soup.new_tag('tr')
                td = soup.new_tag('td')
                td['style'] = (
                    "padding: 16px; "
                    "font-family: Consolas, Monaco, 'Andale Mono', 'Ubuntu Mono', monospace; "
                    "color: #24292e; "
                    "font-size: 13px; "
                    "line-height: 1.6; "
                    "text-align: left; "
                    "word-break: break-all;"
                )
                
                # 5. Insert Content
                card_content = BeautifulSoup(text, 'html.parser')
                td.append(card_content)
                
                tr.append(td)
                table.append(tr)
                
                # 6. Replace original PRE
                pre.replace_with(table)
                
                print("   ✨ Replaced <pre> block with Table-wrapped Prompt Card.")
    
    html_body = str(soup)
    
    try:
        soup = BeautifulSoup(html_body, 'html.parser')
        # Define styles
        list_item_style = "margin: 0 0 10px 0; padding-left: 32px; text-indent: -22px; line-height: 1.7;"
        
        # We want to process P tags. 
        # Since we might split them, we iterate over a list copy
        for p in list(soup.find_all('p')):
            # Skip if already styled
            if p.get('style'):
                continue
                
            text = p.get_text()
            
            # Pattern 1: Chinese Numbers "1、", "2、"
            # Pattern 2: Bullets " - " (space hyphen space) or just " - " at start
            # We'll try to detect if this paragraph looks like a "messy list"
            
            is_messy = False
            delimiter = None
            
            # Check for Chinese numbers
            if len(re.findall(r'(?:^|\s)\d+、', text)) >= 2:
                is_messy = True
                delimiter = r'(?:^|\s)(\d+、)'
            
            # Check for Bullets (e.g. "Title: - Item 1 - Item 2")
            # We look for at least two occurrences of " - "
            elif len(re.findall(r'\s-\s', text)) >= 2:
                is_messy = True
                delimiter = r'(\s-\s)'
            
            if is_messy and delimiter:
                # Split text
                parts = re.split(delimiter, text)
                
                new_tags = []
                current_text = ""
                
                for part in parts:
                    if not part: continue
                    
                    # Check if this part is a delimiter
                    is_delim_match = re.match(delimiter, part) or re.match(r'^\d+、$', part.strip()) or (part.strip() == '-')
                    
                    if re.match(r'^\d+、', part.strip()) or part.strip() == '-':
                        # This is a marker. Start a new paragraph.
                        if current_text:
                            prev_p = soup.new_tag('p')
                            prev_p.string = current_text.strip()
                            # If the previous text started with a marker, style it
                            if re.match(r'^\d+、', current_text.strip()) or current_text.strip().startswith('- '):
                                prev_p['style'] = list_item_style
                            new_tags.append(prev_p)
                        
                        # Start new text with this marker
                        # For bullets, we want to ensure it looks like "- Item"
                        if part.strip() == '-':
                            current_text = "- "
                        else:
                            current_text = part.strip()
                    elif re.match(r'\s-\s', part):
                         # This is the bullet delimiter captured
                        if current_text:
                            prev_p = soup.new_tag('p')
                            prev_p.string = current_text.strip()
                            if re.match(r'^\d+、', current_text.strip()) or current_text.strip().startswith('- '):
                                prev_p['style'] = list_item_style
                            new_tags.append(prev_p)
                        current_text = "- "
                    else:
                        # Content
                        # Ensure NO space after marker to be consistent
                        if current_text and (re.match(r'^\d+、$', current_text.strip()) or current_text.strip() == '-'):
                             part = part.lstrip() # Remove leading space
                        current_text += part
                
                # Last part
                if current_text:
                    last_p = soup.new_tag('p')
                    last_p.string = current_text.strip()
                    if re.match(r'^\d+、', current_text.strip()) or current_text.strip().startswith('- '):
                        last_p['style'] = list_item_style
                    new_tags.append(last_p)
                
                # Replace
                if len(new_tags) > 1:
                    for tag in reversed(new_tags):
                        p.insert_after(tag)
                    p.decompose()
                    
        html_body = str(soup)
        print("   ✨ Fixed inline lists (Chinese numbers and Bullets).")
    except Exception as e:
        print(f"   ⚠️ Inline list fixing failed: {e}")
    
    html_body = str(soup)

    # --- INLINE LIST & FORMATTING FIXING ---
    # Fix paragraphs that contain "1、Text 2、Text" or "- Item - Item" inline.
    try:
        soup = BeautifulSoup(html_body, 'html.parser')
        # Define styles
        list_item_style = "margin: 0 0 10px 0; padding-left: 32px; text-indent: -22px; line-height: 1.7;"
        
        # We want to process P tags. 
        # Since we might split them, we iterate over a list copy
        for p in list(soup.find_all('p')):
            # Skip if already styled
            if p.get('style'):
                continue
                
            text = p.get_text()
            
            # Pattern 1: Chinese Numbers "1、", "2、"
            # Pattern 2: Bullets " - " (space hyphen space) or just " - " at start
            # We'll try to detect if this paragraph looks like a "messy list"
            
            is_messy = False
            delimiter = None
            
            # Check for Chinese numbers
            if len(re.findall(r'(?:^|\s)\d+、', text)) >= 2:
                is_messy = True
                delimiter = r'(?:^|\s)(\d+、)'
            
            # Check for Bullets (e.g. "Title: - Item 1 - Item 2")
            # We look for at least two occurrences of " - "
            elif len(re.findall(r'\s-\s', text)) >= 2:
                is_messy = True
                delimiter = r'(\s-\s)'
            
            if is_messy and delimiter:
                # Split text
                parts = re.split(delimiter, text)
                
                new_tags = []
                current_text = ""
                
                for part in parts:
                    if not part: continue
                    
                    # Check if this part is a delimiter
                    is_delim_match = re.match(delimiter, part) or re.match(r'^\d+、$', part.strip()) or (part.strip() == '-')
                    
                    if re.match(r'^\d+、', part.strip()) or part.strip() == '-':
                        # This is a marker. Start a new paragraph.
                        if current_text:
                            prev_p = soup.new_tag('p')
                            prev_p.string = current_text.strip()
                            # If the previous text started with a marker, style it
                            if re.match(r'^\d+、', current_text.strip()) or current_text.strip().startswith('- '):
                                prev_p['style'] = list_item_style
                            new_tags.append(prev_p)
                        
                        # Start new text with this marker
                        # For bullets, we want to ensure it looks like "- Item"
                        if part.strip() == '-':
                            current_text = "- "
                        else:
                            current_text = part.strip()
                    elif re.match(r'\s-\s', part):
                         # This is the bullet delimiter captured
                        if current_text:
                            prev_p = soup.new_tag('p')
                            prev_p.string = current_text.strip()
                            if re.match(r'^\d+、', current_text.strip()) or current_text.strip().startswith('- '):
                                prev_p['style'] = list_item_style
                            new_tags.append(prev_p)
                        current_text = "- "
                    else:
                        # Content
                        # Ensure NO space after marker to be consistent
                        if current_text and (re.match(r'^\d+、$', current_text.strip()) or current_text.strip() == '-'):
                             part = part.lstrip() # Remove leading space
                        current_text += part
                
                # Last part
                if current_text:
                    last_p = soup.new_tag('p')
                    last_p.string = current_text.strip()
                    if re.match(r'^\d+、', current_text.strip()) or current_text.strip().startswith('- '):
                        last_p['style'] = list_item_style
                    new_tags.append(last_p)
                
                # Replace
                if len(new_tags) > 1:
                    for tag in reversed(new_tags):
                        p.insert_after(tag)
                    p.decompose()
                    
        html_body = str(soup)
        print("   ✨ Fixed inline lists (Chinese numbers and Bullets).")
    except Exception as e:
        print(f"   ⚠️ Inline list fixing failed: {e}")

    # 4. Wrap in Container with CSS
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            /* Reset */
            body {{ margin: 0; padding: 0; }}
            
            /* Theme CSS */
            {css}
            
            /* Ensure images are responsive */
            img {{ max-width: 100%; height: auto; display: block; margin: 20px auto; }}
            
            /* Fix for code blocks: allow scrolling, monospace font by default */
            /* Prompt cards will override this with inline styles */
            pre {{ white-space: pre; overflow-x: auto; -webkit-overflow-scrolling: touch; font-family: Consolas, Monaco, 'Andale Mono', 'Ubuntu Mono', monospace; }}
        </style>
    </head>
    <body>
        {html_body}
    </body>
    </html>
    """
    
    # 5. Inline CSS
    try:
        inlined_html = css_inline.inline(full_html)
        return inlined_html
    except Exception as e:
        print(f"⚠️ CSS Inlining failed: {e}")
        return full_html
