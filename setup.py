import os
import sys
import yaml
import shutil

def setup_interactive():
    print("👋 欢迎使用 md2wechat 快速配置向导！")
    print("-----------------------------------")
    print("本向导将帮助您快速设置环境，让您立即开始创作。\n")

    # 1. WeChat Config
    print("💬 [1/3] 配置微信公众号 (用于自动上传)")
    app_id = input("请输入 AppID (直接回车跳过): ").strip()
    app_secret = input("请输入 AppSecret (直接回车跳过): ").strip()

    # 2. Image Generation Config
    print("\n🎨 [2/3] 配置 AI 生图服务")
    print("请选择您想使用的生图服务提供商：")
    print("1. ModelScope (默认，国内直连，效果好)")
    print("2. OpenAI 兼容接口 (支持 DALL-E, Midjourney, Nano, Seedream 等第三方中转)")
    
    choice = input("请选择 (输入 1 或 2，默认为 1): ").strip()
    
    image_config = {}
    
    if choice == "2":
        # OpenAI Mode
        image_config["image_provider"] = "openai"
        print("\n您选择了 OpenAI 兼容模式。")
        base_url = input("请输入 API Base URL (例如 https://api.openai.com/v1 或第三方中转地址): ").strip()
        if not base_url: base_url = "https://api.openai.com/v1"
        
        api_key = input("请输入 API Key (sk-...): ").strip()
        model = input("请输入模型名称 (例如 dall-e-3, flux, mj-chat): ").strip()
        if not model: model = "dall-e-3"
        
        image_config["image_api_base"] = base_url
        image_config["image_key"] = api_key
        image_config["image_model"] = model
    else:
        # ModelScope Mode
        image_config["image_provider"] = "modelscope"
        print("\n您选择了 ModelScope 模式。")
        print("需要申请 ModelScope API Key (https://modelscope.cn/)")
        api_key = input("请输入 ModelScope API Key: ").strip()
        image_config["image_key"] = api_key
        image_config["image_model"] = "Tongyi-MAI/Z-Image-Turbo"

    # 3. Footer Setup
    print("\n📝 [3/3] 配置文章页脚 (可选)")
    footer_title = input("页脚标题 (例如: 关于作者): ").strip() or "关于作者"
    footer_subtitle = input("页脚副标题 (例如: 专注 AI 技术分享): ").strip() or "专注 AI 技术分享"
    qr_url = input("二维码图片链接 (直接回车跳过): ").strip()
    
    # Create config structure
    config = {
        "app_id": app_id,
        "app_secret": app_secret,
        **image_config, # Merge image config
        "footer": {
            "template": "glass_contact",
            "separator_style": "wave",
            "title": footer_title,
            "subtitle": footer_subtitle,
            "qr_image": qr_url,
            "links": [
                {"text": "示例文章: 如何使用 md2wechat", "url": "#"}
            ]
        }
    }

    # Write to md2wechat.yaml
    config_path = os.path.join(os.getcwd(), "md2wechat.yaml")
    
    # Check if exists
    if os.path.exists(config_path):
        overwrite = input(f"\n⚠️  检测到已存在配置文件 {config_path}，是否覆盖？(y/n): ").lower()
        if overwrite != 'y':
            print("配置已取消。")
            return

    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True, default_flow_style=False)

    print("\n✅ 配置成功！")
    print(f"配置文件已保存至: {config_path}")
    print("\n🚀 接下来您可以：")
    print("1. 运行 python skill/md2wechat/scripts/build.py <您的markdown文件> --upload")
    print("2. 在 Markdown 中使用 ![图](__generate:提示词__) 来测试生图")

if __name__ == "__main__":
    setup_interactive()
