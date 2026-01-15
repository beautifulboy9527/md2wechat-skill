# Footer Assets Library
# Contains SVG separators and HTML footer templates optimized for WeChat

# 1. Dynamic SVG Separators (CSS Animation safe for WeChat)
SVG_SEPARATORS = {
    "wave": """
<svg viewBox="0 0 1440 100" xmlns="http://www.w3.org/2000/svg" style="display: block; width: 100%; height: auto;">
  <style>
    @keyframes wave {
      0% { transform: translateX(0); }
      100% { transform: translateX(-50%); }
    }
    .wave-path {
      animation: wave 10s linear infinite;
    }
  </style>
  <defs>
    <linearGradient id="wave-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#007AFF;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#5856D6;stop-opacity:1" />
    </linearGradient>
  </defs>
  <g class="wave-path" style="width: 200%;">
    <path fill="url(#wave-grad)" fill-opacity="0.2" d="M0,64L48,69.3C96,75,192,85,288,80C384,75,480,53,576,48C672,43,768,53,864,64C960,75,1056,85,1152,80C1248,75,1344,53,1440,48L1440,100L1152,100C1056,100,960,100,864,100C768,100,672,100,576,100C480,100,384,100,288,100C192,100,96,100,48,100L0,100Z"></path>
    <path fill="url(#wave-grad)" fill-opacity="0.2" d="M0,64L48,69.3C96,75,192,85,288,80C384,75,480,53,576,48C672,43,768,53,864,64C960,75,1056,85,1152,80C1248,75,1344,53,1440,48L1440,100L1152,100C1056,100,960,100,864,100C768,100,672,100,576,100C480,100,384,100,288,100C192,100,96,100,48,100L0,100Z" transform="translate(1440, 0)"></path>
  </g>
</svg>
""",
    "neon_pulse": """
<svg viewBox="0 0 800 20" xmlns="http://www.w3.org/2000/svg" style="display: block; margin: 20px auto; width: 80%;">
    <style>
        @keyframes pulse { 0% { opacity: 0.3; width: 10%; } 50% { opacity: 1; width: 100%; } 100% { opacity: 0.3; width: 10%; } }
        .neon-line { animation: pulse 3s ease-in-out infinite; transform-origin: center; }
    </style>
    <rect class="neon-line" x="0" y="8" width="800" height="4" fill="#00f3ff" rx="2" style="filter: drop-shadow(0 0 5px #00f3ff);"/>
</svg>
"""
}

# 2. Footer Templates (Jinja2)
FOOTER_TEMPLATES = {
    "glass_contact": """
<div style="margin-top: 40px; padding: 20px; border-radius: 16px; background: rgba(242, 242, 247, 0.8); border: 1px solid rgba(0,0,0,0.05); text-align: center; font-family: -apple-system, sans-serif;">
    {{ separator }}
    <div style="margin: 20px 0;">
        <h3 style="margin: 0; font-size: 18px; color: #1D1D1F;">{{ title }}</h3>
        <p style="margin: 8px 0 0; font-size: 14px; color: #86868b;">{{ subtitle }}</p>
    </div>
    
    {% if qr_image %}
    <div style="margin: 20px auto; width: 160px; height: 160px; padding: 10px; background: #fff; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
        <img src="{{ qr_image }}" style="width: 100%; height: 100%; display: block;">
    </div>
    {% endif %}

    {% if links %}
    <div style="margin-top: 20px; padding-top: 20px; border-top: 1px dashed rgba(0,0,0,0.1);">
        <p style="font-size: 12px; color: #86868b; margin-bottom: 10px;">往期推荐</p>
        {% for link in links %}
        <a href="{{ link.url }}" style="display: block; margin: 8px 0; font-size: 14px; color: #007AFF; text-decoration: none;">{{ link.text }}</a>
        {% endfor %}
    </div>
    {% endif %}
</div>
""",
    "simple_ad": """
<div style="margin-top: 50px; text-align: center;">
    {{ separator }}
    <div style="margin: 20px auto; max-width: 300px; border: 2px dashed #ddd; padding: 15px; border-radius: 8px;">
        <p style="font-size: 14px; color: #666; margin: 0;">{{ ad_text }}</p>
        <a href="{{ ad_link }}" style="display: inline-block; margin-top: 10px; padding: 6px 16px; background: #333; color: #fff; text-decoration: none; border-radius: 4px; font-size: 12px;">了解更多</a>
    </div>
</div>
"""
}

def get_footer(template_name, context):
    """
    Render a footer template with the given context.
    context: dict containing title, subtitle, qr_image, links, etc.
    """
    from jinja2 import Template
    
    # Determine template based on 'type' if present, otherwise use 'template'
    ftype = context.get("type")
    if ftype == "ad":
        template_name = "simple_ad"
    elif ftype == "qr":
        template_name = "glass_contact"
    # else use provided template_name or default
    
    template_str = FOOTER_TEMPLATES.get(template_name, FOOTER_TEMPLATES["glass_contact"])
    
    # Inject separator if requested
    separator_key = context.get("separator_style")
    if separator_key and separator_key in SVG_SEPARATORS:
        context["separator"] = SVG_SEPARATORS[separator_key]
    else:
        context["separator"] = ""
        
    template = Template(template_str)
    return template.render(**context)

