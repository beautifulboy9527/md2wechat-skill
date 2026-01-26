import argparse
import os
import datetime
import re
import sys

# Add parent dir to path to import prompts
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import prompts

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')

def create_draft(topic, writer_type="pm", output_dir="drafts"):
    date_str = datetime.datetime.now().strftime("%Y%m%d")
    slug = slugify(topic)
    draft_dir = os.path.join(output_dir, f"{date_str}_{slug}")
    
    if not os.path.exists(draft_dir):
        os.makedirs(draft_dir)
        
    filename = os.path.join(draft_dir, f"{slug}.md")
    
    # Select Prompts
    if writer_type == "tech":
        system_prompt = prompts.TECH_SYSTEM_PROMPT
        theme = "tech-docs" # or default
        cover_style = "tech"
        cover_sub_style = "sci_fi"
    else:
        system_prompt = prompts.PM_SYSTEM_PROMPT
        theme = "chinese-scroll" # or default
        cover_style = "illustration"
        cover_sub_style = "notion"
        
    # Prepare Content
    structure_prompt = prompts.STRUCTURE_MAP_PROMPT_TEMPLATE.format(topic=topic)
    # Escape newlines for the one-line generate syntax
    structure_prompt_oneline = structure_prompt.replace('\n', ' ').strip()
    
    cover_prompt = prompts.COVER_PROMPT_TEMPLATE.format(
        topic=topic, 
        style=cover_style, 
        title=topic, 
        subtitle="Deep Dive", 
        visual_elements="abstract shapes"
    ).replace('\n', ' ').strip()

    content = f"""---
title: {topic}
date: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
theme: {theme}
cover:
  prompt: "{cover_prompt}"
  style: {cover_style}
  sub_style: {cover_sub_style}
---

<!-- 
SYSTEM PROMPT (For AI Writer):
{system_prompt}
-->

# {topic}

![Cover Image](__generate:{cover_prompt}|size=16:9__)

![Structure Map](__generate:{structure_prompt_oneline}|style=graphic_recording|size=16:9__)

## 1. 背景与痛点

(在这里描述为什么写这篇文章，遇到的问题是什么...)

## 2. 核心观点

(你的核心看法...)

## 3. 详细分析

(具体的内容...)

## 4. 总结与建议

(给读者的建议...)

"""
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"✅ Draft created at: {filename}")
    print(f"📂 Directory: {draft_dir}")
    print("👉 Next steps:")
    print("1. Open the file.")
    print("2. Use the System Prompt to guide the AI to fill in the sections.")
    print("3. Run 'python skill/md2wechat/scripts/build.py <file>' to generate images and preview.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a new article draft with Writer prompts")
    parser.add_argument("topic", help="Article topic")
    parser.add_argument("--type", choices=["pm", "tech"], default="pm", help="Writer type (pm or tech)")
    parser.add_argument("--out", default="drafts", help="Output directory")
    
    args = parser.parse_args()
    create_draft(args.topic, args.type, args.out)
