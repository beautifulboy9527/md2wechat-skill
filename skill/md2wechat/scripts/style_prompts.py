# Style Prompts Library
# Contains prompt engineering knowledge for various styles

IMAGE_STYLES = {
    "tech": {
        "name": "科技未来",
        "prompt_suffix": ", futuristic, sci-fi, cyberpunk, neon lights, high tech, mechanical details, sharp edges, 8k resolution, unreal engine 5 render",
        "sub_styles": {
            "sci_fi": "mechanical edges, streamline design, neon accents, sharp corners, metal texture, chip patterns",
            "virtual": "dark background, digital deconstruction, cut lines, future tech visual",
            "data": "dark blue tech background, digital matrix, holographic projection, circuit board elements",
            "blueprint": "blue engineering blueprint background, technical lines, precise geometric structure, white highlight text"
        }
    },
    "art": {
        "name": "艺术情感",
        "prompt_suffix": ", artistic, abstract, elegant, emotional, high quality, detailed, masterpiece",
        "sub_styles": {
            "ink": "traditional chinese ink painting, watercolor, scroll style, minimalist, zen, negative space",
            "impressionism": "soft natural light, impressionist painting texture, dappled light and shadow, warm dreamy atmosphere",
            "smoke": "light smoke curling, semi-transparent gradient, flowing texture, hazy dreamy atmosphere",
            "flowing_gaze": "minimalist line art, vintage book cover aesthetic, woodcut texture, stippling shading, radical perspective shift, worm's eye view or top-down view, vast negative space, surreal, melancholic"
        }
    },
    "fashion": {
        "name": "时尚杂志",
        "prompt_suffix": ", high fashion photography, vogue style, bold colors, high contrast, studio lighting, 8k, masterpiece",
        "sub_styles": {
            "bold": "neon colors, dark background, geometric shapes, asymmetric composition, cyberpunk vibes",
            "minimal": "clean white background, helvetica font, minimalist composition, high key lighting"
        }
    },
    "cute": {
        "name": "活泼可爱",
        "prompt_suffix": ", cute, colorful, vibrant, cartoon style, soft lighting, 3d render, clay texture",
        "sub_styles": {
            "pop": "bright summer colors, lively hand-drawn style, watercolor splash, scene elements",
            "candy": "bright candy colors, candy collage, colorful, sweet and happy atmosphere",
            "doodle": "colorful graffiti art, thick bold outlines, dynamic structure, hand-drawn print style"
        }
    },
    "industrial": {
        "name": "工业质感",
        "prompt_suffix": ", industrial, metallic, rusty, heavy machinery, steam punk, grunge, textured",
        "sub_styles": {
            "metal": "rough metal texture, rust spots, relief structure, mechanical craft, rivet details",
            "cyber_game": "shocking electric effect, dark blue-purple tone, 3d relief, lightning energy, strong sci-fi game feel"
        }
    },
    "retro": {
        "name": "复古怀旧",
        "prompt_suffix": ", retro, vintage, old photo, grainy, noise, classic, 1980s style",
        "sub_styles": {
            "pixel": "retro game pixel style, bright contrast colors, block splicing, castle game scene",
            "classic": "gothic variation, slender vertical proportions, sharp straight lines, rich decorative details",
            "woodblock": "natural rough edges, strong wood carving feel, warm and rustic atmosphere"
        }
    },
    "nature": {
        "name": "自然元素",
        "prompt_suffix": ", nature, organic, plants, flowers, landscape, natural light, photorealistic",
        "sub_styles": {
            "wood": "forest green background, wood texture, organic natural form, vine leaf decoration",
            "frost": "winter snow background, ice crystal effect, cold tone, semi-transparent texture"
        }
    }
}

# HTML Templates
APPLE_BENTO_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=1000, initial-scale=1.0">
    <title>Card</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Sans+SC:wght@400;500;700;900&display=swap');
        :root {
            --glass-bg: rgba(255, 255, 255, 0.25);
            --glass-border: rgba(255, 255, 255, 0.4);
            --glass-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
            --primary-blue: #007AFF;
        }
        body {
            background-color: #F2F2F7;
            font-family: 'SF Pro Display', 'Inter', 'Noto Sans SC', sans-serif;
            margin: 0;
            padding: 40px;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background-image: radial-gradient(circle at 10% 20%, rgba(0, 122, 255, 0.1) 0%, transparent 40%), radial-gradient(circle at 90% 80%, rgba(88, 86, 214, 0.1) 0%, transparent 40%);
        }
        .glass-card {
            background: var(--glass-bg);
            backdrop-filter: blur(30px) saturate(180%);
            border: 1px solid var(--glass-border);
            border-radius: 28px;
            padding: 40px;
            box-shadow: var(--glass-shadow);
            width: 800px;
            position: relative;
            overflow: hidden;
        }
        h1 { font-size: 48px; font-weight: 800; color: #1D1D1F; margin-bottom: 16px; }
        p { font-size: 20px; line-height: 1.6; color: #1D1D1F; opacity: 0.85; }
    </style>
</head>
<body>
    <div class="glass-card">
        <h1>{{ title }}</h1>
        <p>{{ content }}</p>
    </div>
</body>
</html>
"""

MERMAID_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>mermaid.initialize({startOnLoad:true, theme: 'neutral'});</script>
    <style>
        body { margin: 0; padding: 20px; background: white; font-family: sans-serif; }
        .mermaid { display: flex; justify-content: center; }
    </style>
</head>
<body>
    <div class="mermaid">
        {{ content }}
    </div>
</body>
</html>
"""


NEON_CARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=1000, initial-scale=1.0">
    <title>Neon Card</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Noto+Sans+SC:wght@400;700&display=swap');
        body {
            margin: 0; padding: 40px; min-height: 100vh;
            display: flex; justify-content: center; align-items: center;
            background: #050510;
            font-family: 'Orbitron', 'Noto Sans SC', sans-serif;
        }
        .card {
            background: rgba(10, 10, 20, 0.8);
            border: 2px solid #00f3ff;
            box-shadow: 0 0 20px rgba(0, 243, 255, 0.3), inset 0 0 20px rgba(0, 243, 255, 0.1);
            border-radius: 12px;
            padding: 40px;
            width: 800px;
            position: relative;
            color: #fff;
        }
        .card::before {
            content: ''; position: absolute; top: -2px; left: 20px; right: 20px; height: 2px;
            background: #00f3ff; box-shadow: 0 0 10px #00f3ff;
        }
        h1 {
            font-size: 48px; margin: 0 0 20px 0;
            text-shadow: 0 0 10px #d000ff;
            color: #d000ff;
            text-transform: uppercase;
        }
        p { font-size: 20px; line-height: 1.6; color: #e0e0e0; text-shadow: 0 0 5px rgba(255,255,255,0.5); }
    </style>
</head>
<body>
    <div class="card">
        <h1>{{ title }}</h1>
        <p>{{ content }}</p>
    </div>
</body>
</html>
"""

BRUTAL_CARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=1000, initial-scale=1.0">
    <title>Brutal Card</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Noto+Sans+SC:wght@700;900&display=swap');
        body {
            margin: 0; padding: 40px; min-height: 100vh;
            display: flex; justify-content: center; align-items: center;
            background: #fff;
            font-family: 'Space Mono', 'Noto Sans SC', monospace;
        }
        .card {
            background: #ff0;
            border: 8px solid #000;
            box-shadow: 16px 16px 0 #000;
            padding: 40px;
            width: 800px;
            color: #000;
            transform: rotate(-1deg);
        }
        h1 {
            font-size: 56px; margin: 0 0 20px 0;
            background: #000; color: #fff;
            display: inline-block; padding: 10px 20px;
            transform: rotate(2deg);
        }
        p { font-size: 24px; line-height: 1.4; font-weight: 700; border-top: 4px solid #000; padding-top: 20px; }
    </style>
</head>
<body>
    <div class="card">
        <h1>{{ title }}</h1>
        <p>{{ content }}</p>
    </div>
</body>
</html>
"""

ORIENTAL_CARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=1000, initial-scale=1.0">
    <title>Oriental Card</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&display=swap');
        body {
            margin: 0; padding: 40px; min-height: 100vh;
            display: flex; justify-content: center; align-items: center;
            background: #f4f1ea;
            font-family: 'Noto Serif SC', serif;
        }
        .card {
            background: #fff;
            padding: 60px 80px;
            width: 600px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.05);
            position: relative;
            writing-mode: vertical-rl;
            min-height: 500px;
            border-left: 1px solid #a00;
        }
        h1 {
            font-size: 42px; margin: 0 0 0 40px;
            color: #333;
            border-top: 4px solid #a00;
            padding-top: 20px;
        }
        p { font-size: 20px; line-height: 2; color: #666; letter-spacing: 2px; }
        .seal {
            position: absolute; bottom: 40px; left: 40px;
            width: 60px; height: 60px;
            border: 2px solid #a00;
            color: #a00;
            display: flex; justify-content: center; align-items: center;
            font-weight: bold;
            border-radius: 4px;
            writing-mode: horizontal-tb;
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>{{ title }}</h1>
        <p>{{ content }}</p>
        <div class="seal">印</div>
    </div>
</body>
</html>
"""

MAGAZINE_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=1000, initial-scale=1.0">
    <title>Magazine Card</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Helvetica+Neue:wght@400;700;900&family=Noto+Sans+SC:wght@400;700;900&display=swap');
        body {
            margin: 0; padding: 40px; min-height: 100vh;
            display: flex; justify-content: center; align-items: center;
            background: #f0f2f5;
            font-family: 'Helvetica Neue', 'Noto Sans SC', sans-serif;
        }
        .card {
            background: #050505;
            color: #ffffff;
            padding: 60px;
            width: 800px;
            box-shadow: 0 20px 50px rgba(0,0,0,0.3);
            position: relative;
        }
        h1 {
            font-size: 64px; margin: 0 0 30px 0;
            color: #ccff00;
            text-transform: uppercase;
            letter-spacing: -2px;
            line-height: 0.9;
            border-top: 10px solid #00ccff;
            padding-top: 30px;
        }
        p { font-size: 24px; line-height: 1.6; color: #eeeeee; }
    </style>
</head>
<body>
    <div class="card">
        <h1>{{ title }}</h1>
        <p>{{ content }}</p>
    </div>
</body>
</html>
"""

# Theme Mapping Configuration
THEME_MAPPING = {
    "default": {
        "image_style": "art",
        "image_sub_style": "impressionism",
        "html_template": "apple"
    },
    "twilight": {
        "image_style": "art",
        "image_sub_style": "impressionism",
        "html_template": "apple" # Fallback to apple for now, or create specific
    },
    "brutalism": {
        "image_style": "industrial",
        "image_sub_style": None, # Use default industrial
        "html_template": "brutal"
    },
    "chinese-scroll": {
        "image_style": "art",
        "image_sub_style": "ink",
        "html_template": "oriental"
    },
    "cyber": {
        "image_style": "tech",
        "image_sub_style": "sci_fi",
        "html_template": "neon"
    },
    "minimalist": {
        "image_style": "art",
        "image_sub_style": "impressionism",
        "html_template": "apple"
    },
    "fashion": {
        "image_style": "fashion",
        "image_sub_style": "bold",
        "html_template": "magazine"
    }
}

def get_style_prompt(style_key, sub_style=None):
    style = IMAGE_STYLES.get(style_key)
    if not style:
        return ""
    
    suffix = style["prompt_suffix"]
    if sub_style and sub_style in style["sub_styles"]:
        suffix += ", " + style["sub_styles"][sub_style]
    
    return suffix

def get_html_template(template_name):
    if template_name == "apple":
        return APPLE_BENTO_TEMPLATE
    elif template_name == "mermaid":
        return MERMAID_TEMPLATE
    elif template_name == "neon":
        return NEON_CARD_TEMPLATE
    elif template_name == "brutal":
        return BRUTAL_CARD_TEMPLATE
    elif template_name == "oriental":
        return ORIENTAL_CARD_TEMPLATE
    elif template_name == "magazine":
        return MAGAZINE_TEMPLATE
    return APPLE_BENTO_TEMPLATE # Default

def get_theme_config(theme_name):
    return THEME_MAPPING.get(theme_name, THEME_MAPPING["default"])

