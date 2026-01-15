import os
import sys
import yaml
import shutil

def setup_interactive():
    print("👋 欢迎使用 md2wechat 快速配置向导！")
    print("-----------------------------------")
    print("本向导将帮助您快速设置 API Key 和页脚信息，让您立即开始创作。\n")

    # 1. API Key Setup
    print("🔑 [1/3] 配置 AI 绘图 (ModelScope)")
    print("为了使用 AI 自动生成封面图，我们需要您的 ModelScope API Key。")
    print("如果您还没有，可以跳过，但无法使用自动生图功能。")
    api_key = input("请输入您的 API Key (直接回车跳过): ").strip()

    # 1.5 WeChat Config
    print("\n💬 [1.5/3] 配置微信公众号 (可选，用于自动上传)")
    app_id = input("请输入 AppID (直接回车跳过): ").strip()
    app_secret = input("请输入 AppSecret (直接回车跳过): ").strip()


    # 2. Footer Setup
    print("\n📝 [2/3] 配置文章页脚")
    print("页脚将显示在每篇文章底部，用于展示您的公众号信息或广告。")
    footer_title = input("页脚标题 (例如: 关于作者): ").strip() or "关于作者"
    footer_subtitle = input("页脚副标题 (例如: 专注 AI 技术分享): ").strip() or "专注 AI 技术分享"
    
    print("\n🔗 [3/3] 配置二维码与链接")
    qr_url = input("二维码图片链接 (直接回车跳过): ").strip()
    
    # Create config structure
    config = {
        "image_key": api_key,
        "app_id": app_id,
        "app_secret": app_secret,
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
    print("\n🚀 您现在可以尝试运行: python skill/md2wechat/scripts/build.py promotion.md")

if __name__ == "__main__":
    setup_interactive()
