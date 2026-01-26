# Style Prompts Library
# Contains prompt engineering knowledge for various styles

IMAGE_STYLES = {
    "tech": {
        "name": "科技未来",
        "prompt_suffix": ", futuristic, sci-fi, cyberpunk, neon lighting, mechanical details, sharp focus, cinematic composition, unreal engine 5 render",
        "sub_styles": {
            "sci_fi": "mechanical edges, streamline design, neon accents, sharp corners, metal texture, chip patterns, industrial lighting",
            "virtual": "dark background, digital deconstruction, cut lines, future tech visual, volumetric lighting",
            "data": "dark blue tech background, digital matrix, holographic projection, circuit board elements, depth of field",
            "blueprint": "precise technical blueprint style, engineering aesthetic, precise lines with consistent stroke weights, technical schematics, clean vector graphics, dimension lines, measurement indicators, grid alignment, geometric precision, clean sans-serif hand lettering, engineering blue and white",
            "hologram": "dark tech background, holographic rainbow effect, spectral gradient, futuristic, ethereal glow"
        }
    },
    "art": {
        "name": "艺术情感",
        "prompt_suffix": ", artistic, abstract, elegant, emotional, detailed texture, professional lighting, museum quality",
        "sub_styles": {
            "ink": "traditional chinese ink painting, watercolor, scroll style, minimalist, zen, negative space, wet wash",
            "impressionism": "soft natural light, impressionist painting texture, dappled light and shadow, warm atmosphere, visible brushstrokes",
            "smoke": "light smoke curling, semi-transparent gradient, flowing texture, hazy atmosphere, ethereal",
            "flowing_gaze": "minimalist line art, vintage book cover aesthetic, woodcut texture, stippling shading, radical perspective shift, worm's eye view or top-down view, vast negative space, surreal, melancholic",
            "washi": "traditional japanese paper texture, brush calligraphy, zen negative space, tea room atmosphere, soft fibers",
            "paper_cut": "festive red background, traditional paper cutting craft, gold accents, auspicious clouds, layered paper depth"
        }
    },
    "fashion": {
        "name": "时尚杂志",
        "prompt_suffix": ", high fashion photography, vogue style, bold colors, high contrast, studio lighting, professional color grading",
        "sub_styles": {
            "bold": "high impact, attention-grabbing, vibrant red orange yellow palette, dark background, exclamation marks, arrows, warning icons, strong shapes, high contrast elements, dramatic compositions, bold impactful hand lettering",
            "minimal": "ultra-clean, sophisticated, black and white with single accent color, single focal point, thin lines, maximum whitespace, simple clean decorations, clean simple hand lettering"
        }
    },
    "cute": {
        "name": "活泼可爱",
        "prompt_suffix": ", cute, colorful, vibrant, cartoon style, soft lighting, 3d render, clay texture, c4d render",
        "sub_styles": {
            "pop": "vibrant, energetic, eye-catching, bright red yellow blue palette, bold shapes, speech bubbles, comic-style effects, starburst, dynamic energetic compositions, dynamic hand lettering with outlines",
            "candy": "bright candy colors, candy collage, colorful, sweet atmosphere, pastel tones",
            "doodle": "colorful graffiti art, thick bold outlines, dynamic structure, hand-drawn print style, marker texture"
        }
    },
    "industrial": {
        "name": "工业质感",
        "prompt_suffix": ", industrial, metallic, rusty, heavy machinery, steam punk, grunge, textured, dramatic lighting",
        "sub_styles": {
            "metal": "rough metal texture, rust spots, relief structure, mechanical craft, rivet details, macro shot",
            "cyber_game": "shocking electric effect, dark blue-purple tone, 3d relief, lightning energy, strong sci-fi game feel, bloom effect"
        }
    },
    "retro": {
        "name": "复古怀旧",
        "prompt_suffix": ", retro, vintage, old photo, grainy, noise, classic, 1980s style, film photography",
        "sub_styles": {
            "pixel": "retro 8-bit pixel art aesthetic, nostalgic gaming style, visible pixel structure, simple iconography, text bubbles with pixel borders, progress bars with chunky segments, dithering patterns, limited 16-32 color palette, pixelated bitmap font style",
            "classic": "gothic variation, slender vertical proportions, sharp straight lines, rich decorative details, etching style",
            "woodblock": "natural rough edges, strong wood carving feel, warm and rustic atmosphere, linocut",
            "mosaic": "retro tile collage, square pixel structure, color blocks, retro gaming feel, ceramic texture"
        }
    },
    "nature": {
        "name": "自然元素",
        "prompt_suffix": ", nature, organic, plants, flowers, landscape, natural light, photorealistic, macro photography",
        "sub_styles": {
            "wood": "forest green background, wood texture, organic natural form, vine leaf decoration, sunlight filtering through leaves",
            "frost": "winter snow background, ice crystal effect, cold tone, semi-transparent texture, bokeh",
            "stardust": "deep space galaxy, stardust particles, milky way light, cosmic energy, nebula"
        }
    },
    "illustration": {
        "name": "插画风格",
        "prompt_suffix": ", high quality illustration, vector art, clean lines, professional design, trending on dribbble",
        "sub_styles": {
            "notion": "minimalist hand-drawn line art, intellectual style, clean SaaS dashboard aesthetic, simple line doodles, hand-drawn wobble effect, geometric shapes, stick figures, maximum whitespace, single-weight ink lines, clean hand-drawn lettering, black and white with pastel accents",
            "flat": "cute simple doodle illustrations, bold black outlines, simple flat shapes, no shading, cute rounded proportions, productivity-themed icons, isolated elements on white background, minimal decorative details, bright pastel colors",
            "watercolor": "soft watercolor illustration style, hand-painted textures, watercolor washes, visible brush strokes, natural elements, leaves flowers organic shapes, color bleeds, soft edges, elegant handwritten script, soft coral and dusty rose palette",
            "chalkboard": "black chalkboard background, colorful chalk drawing style, hand-drawn chalk illustrations, sketchy imperfect lines, chalk dust effects, eraser smudges, white or bright colored chalk text, authentic chalkboard texture",
            "clay": "3d claymation style, soft plasticine texture, rounded edges, fingerprint details, stop-motion aesthetic, soft studio lighting, pastel colors, cute and playful"
        }
    },
    "graphic_recording": {
        "name": "视觉记录",
        "prompt_suffix": ", graphic recording style, visual thinking, hand-drawn sketch, white background, black fine-tip pen outlines, colored markers (cyan, orange, soft red), visual metaphors, arrows connecting ideas, clear structure, business doodle style",
        "sub_styles": {
            "default": "clean white paper, marker coloring, mind map structure",
            "sketch": "rough pencil sketch, artistic, creative process feel"
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

XHS_CARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=750, initial-scale=1.0">
    <title>XHS Card</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700;900&display=swap');
        body {
            margin: 0; padding: 0;
            width: 750px; height: 1334px;
            background: linear-gradient(135deg, #F8BBD9 0%, #E4A0B7 50%, #C7CEEA 100%);
            font-family: 'Noto Sans SC', sans-serif;
            display: flex; justify-content: center; align-items: center;
        }
        .card {
            width: 650px; height: 1200px;
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(20px);
            border-radius: 40px;
            padding: 50px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.1);
            position: relative;
            display: flex; flex-direction: column;
        }
        .header { margin-bottom: 40px; text-align: center; }
        h1 { font-size: 56px; color: #1A1A1A; margin: 0 0 20px 0; letter-spacing: -1px; }
        .subtitle { font-size: 32px; color: #555; font-weight: 500; }
        .content { flex: 1; font-size: 28px; line-height: 1.6; color: #333; }
        .highlight { color: #FF6B35; font-weight: bold; }
        .footer { margin-top: auto; text-align: center; font-size: 24px; color: #888; }
        .decoration {
            position: absolute; width: 200px; height: 200px;
            background: linear-gradient(45deg, #A8DADC, #457B9D);
            border-radius: 50%; filter: blur(40px); opacity: 0.6;
            top: -50px; right: -50px; z-index: -1;
        }
    </style>
</head>
<body>
    <div class="decoration"></div>
    <div class="card">
        <div class="header">
            <h1>{{ title }}</h1>
            <div class="subtitle">✨ 核心知识点 ✨</div>
        </div>
        <div class="content">
            {{ content }}
        </div>
        <div class="footer">
            @Antigravity • 知识分享
        </div>
    </div>
</body>
</html>
"""

VINTAGE_CARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=750, initial-scale=1.0">
    <title>Vintage Card</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&family=Long+Cang&display=swap');
        body {
            margin: 0; padding: 0;
            width: 750px; height: 1334px;
            background-color: #F5F5DC;
            background-image: linear-gradient(rgba(0,0,0,0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(0,0,0,0.05) 1px, transparent 1px);
            background-size: 30px 30px;
            font-family: 'Noto Serif SC', serif;
            display: flex; justify-content: center; align-items: center;
        }
        .paper {
            width: 650px; height: 1200px;
            background: #FFFFF0;
            padding: 60px;
            box-shadow: 5px 5px 15px rgba(0,0,0,0.1);
            border: 1px solid #D2B48C;
            position: relative;
        }
        .paper::before {
            content: ''; position: absolute; top: 0; left: 40px; bottom: 0; width: 2px;
            background: #FF9999; opacity: 0.5;
        }
        h1 {
            font-family: 'Noto Serif SC', serif;
            font-size: 52px; color: #2F4F4F;
            border-bottom: 3px double #2F4F4F;
            padding-bottom: 20px; margin-bottom: 40px;
            text-align: center;
        }
        .content { font-size: 26px; line-height: 1.8; color: #333; }
        .handwritten {
            font-family: 'Long Cang', cursive;
            color: #8B4513; font-size: 30px;
            transform: rotate(-2deg);
            display: inline-block;
        }
        .stamp {
            position: absolute; bottom: 60px; right: 60px;
            border: 3px solid #B22222; color: #B22222;
            padding: 10px 20px; font-weight: bold;
            transform: rotate(-15deg); opacity: 0.8;
            font-size: 24px; border-radius: 4px;
        }
    </style>
</head>
<body>
    <div class="paper">
        <h1>{{ title }}</h1>
        <div class="content">
            {{ content }}
            <br><br>
            <p class="handwritten">Notes: 重点记忆</p>
        </div>
        <div class="stamp">APPROVED</div>
    </div>
</body>
</html>
"""

MEMPHIS_CARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=750, initial-scale=1.0">
    <title>Memphis Card</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@900&display=swap');
        body {
            margin: 0; padding: 0;
            width: 750px; height: 1334px;
            background: #FFF;
            font-family: 'Noto Sans SC', sans-serif;
            overflow: hidden;
        }
        .shape1 {
            position: absolute; top: -100px; right: -100px;
            width: 400px; height: 400px; background: #FFDD00;
            border-radius: 50%; border: 4px solid #000;
        }
        .shape2 {
            position: absolute; bottom: 100px; left: -50px;
            width: 300px; height: 300px; background: #0052FF;
            transform: rotate(45deg); border: 4px solid #000;
        }
        .card {
            position: relative; z-index: 10;
            margin: 100px 50px;
            background: #FFF;
            border: 4px solid #000;
            box-shadow: 15px 15px 0 #000;
            padding: 40px;
            height: 1000px;
        }
        h1 {
            font-size: 60px; line-height: 1.2; margin-bottom: 40px;
            color: #000; text-transform: uppercase;
            background: #FF69B4; display: inline;
            box-shadow: 5px 5px 0 #000;
            padding: 5px 10px;
        }
        .content {
            font-size: 28px; line-height: 1.6; color: #000; margin-top: 40px;
            font-weight: bold;
        }
        .dots {
            position: absolute; top: 20px; left: 20px;
            width: 100px; height: 100px;
            background-image: radial-gradient(#000 20%, transparent 20%);
            background-size: 10px 10px; opacity: 0.2;
        }
    </style>
</head>
<body>
    <div class="shape1"></div>
    <div class="shape2"></div>
    <div class="card">
        <div class="dots"></div>
        <h1>{{ title }}</h1>
        <div class="content">
            {{ content }}
        </div>
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
    },
    "xhs-note": {
        "image_style": "cute",
        "image_sub_style": "pop",
        "html_template": "xhs"
    },
    "vintage-journal": {
        "image_style": "retro",
        "image_sub_style": "woodblock",
        "html_template": "vintage"
    },
    "memphis-pop": {
        "image_style": "cute",
        "image_sub_style": "pop",
        "html_template": "memphis"
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
    elif template_name == "xhs":
        return XHS_CARD_TEMPLATE
    elif template_name == "vintage":
        return VINTAGE_CARD_TEMPLATE
    elif template_name == "memphis":
        return MEMPHIS_CARD_TEMPLATE
    return APPLE_BENTO_TEMPLATE # Default

def get_theme_config(theme_name):
    return THEME_MAPPING.get(theme_name, THEME_MAPPING["default"])

