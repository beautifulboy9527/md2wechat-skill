import argparse
import os
import sys
import yaml
# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import footer_assets

def append_footer(html_file, config_file=None):
    # 1. Load Config
    config = {
        "template": "glass_contact",
        "separator_style": "wave",
        "title": "感谢阅读",
        "subtitle": "关注公众号，获取更多 AI 实战干货",
        "qr_image": "", # Optional path to QR code
        "links": [] # Optional list of {text, url}
    }
    
    if config_file and os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            user_config = yaml.safe_load(f)
            if user_config and "footer" in user_config:
                config.update(user_config["footer"])
    
    # 2. Render Footer
    footer_html = footer_assets.get_footer(config["template"], config)
    
    # 3. Append to HTML File
    if os.path.exists(html_file):
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Insert before </body> if present, otherwise append
        if "</body>" in content:
            new_content = content.replace("</body>", f"{footer_html}\n</body>")
        else:
            new_content = content + "\n" + footer_html
            
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Successfully appended footer to {html_file}")
    else:
        print(f"Error: HTML file {html_file} not found")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Append footer to HTML article")
    parser.add_argument("html_file", help="Path to the HTML file")
    parser.add_argument("--config", help="Path to config yaml (optional)")
    
    args = parser.parse_args()
    append_footer(args.html_file, args.config)
