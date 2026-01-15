# md2wechat Skill

<div align="center">

**用 Markdown 写公众号文章，像发朋友圈一样简单**

[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

</div>

---

## 🚀 30 秒快速开始

**小白用户只需 3 步：**

```bash
# 1. 克隆项目
git clone https://github.com/beautifulboy9527/md2wechat-skill.git
cd md2wechat-skill

# 2. 安装依赖 (一键完成)
pip install -r requirements.txt
playwright install chromium

# 3. 运行配置向导 (跟着提示输入即可)
python setup.py
```

配置完成后，创建一个 `article.md` 文件，然后运行：
```bash
python skill/md2wechat/scripts/build.py article.md
```
打开生成的 `article_wechat.html` 预览效果！

---

## ✨ 功能一览

| 功能 | 说明 | 使用方法 |
|------|------|----------|
| 📝 **Markdown 排版** | 用 Markdown 写作，自动转换为精美 HTML | 默认功能 |
| 🎨 **多主题切换** | 内置卷轴风、科技风、暮光等多种风格 | 在文件头部加 `theme: chinese-scroll` |
| 🖼️ **AI 封面生成** | 根据提示词自动生成封面图 | 在文件头部配置 `cover.prompt` |
| 📸 **卡片模式** | 全文渲染为高清图片卡片，适合设计海报 | 命令加 `--mode image` |
| 🦶 **动态页脚** | 自动添加二维码、广告或历史文章 | 在配置中设置 `footer` |
| 🚀 **一键上传** | 直接发送到微信公众号草稿箱 | 命令加 `--upload` |

---

## 📖 使用指南

### 方式一：最简单 (只排版)
直接写 Markdown，运行命令：
```bash
python skill/md2wechat/scripts/build.py my_article.md
```

### 方式二：带配置 (推荐)
在 Markdown 文件顶部添加配置：
```markdown
---
theme: twilight                 # 主题：twilight, chinese-scroll, brutalism, cyber
title: 我的文章标题              # 文章标题
cover:
  prompt: "一只在写代码的猫"      # AI 生成封面的提示词
  style: ink                    # 封面风格：ink (水墨), sci_fi (科幻)
footer:
  type: qr                      # 页脚类型：qr (二维码) 或 ad (广告)
  title: 关注我的公众号
  qr_image: https://example.com/qr.png
---

# 正文开始

这里是你的文章内容...
```

然后运行：
```bash
python skill/md2wechat/scripts/build.py my_article.md --upload
```

### 方式三：卡片长图模式
适合制作精美的海报式文章：
```bash
python skill/md2wechat/scripts/build.py my_article.md --mode image --upload
```
这会将文章按章节切分，每个章节渲染为一张高清图片。

---

## ⚙️ 配置说明

### 全局配置 (`md2wechat.yaml`)
运行 `python setup.py` 会自动生成，也可手动编辑：

```yaml
# AI 绘图 API Key (可选，用于生成封面)
image_key: "sk-xxxx"

# 微信公众号 (可选，用于一键上传)
app_id: "wx-xxxx"
app_secret: "xxxx"

# 默认页脚
footer:
  type: qr                      # qr 或 ad
  title: "关于作者"
  subtitle: "专注技术分享"
  qr_image: "https://..."
```

### 页脚类型切换
**每篇文章可以不同！** 在 Markdown 头部覆盖：

**今天发广告：**
```yaml
footer:
  type: ad
  ad_text: "新课上线，限时 5 折！"
  ad_link: "https://..."
```

**明天发二维码：**
```yaml
footer:
  type: qr
  title: "加入社群"
  qr_image: "https://..."
```

---

## ❓ 常见问题

**Q: 运行报错 `ModuleNotFoundError`**
A: 请确保运行了 `pip install -r requirements.txt`

**Q: HTML 截图失败**
A: 请确保运行了 `playwright install chromium`

**Q: 上传失败**
A: 检查 `md2wechat.yaml` 中的 `app_id` 和 `app_secret` 是否正确，且服务器 IP 已加入公众号白名单

**Q: 主题不生效**
A: 确保 `theme` 名称正确（如 `twilight`, `chinese-scroll`, `brutalism`）

---

## 📂 目录结构

```
md2wechat-skill/
├── setup.py                 # 配置向导 (小白入口)
├── requirements.txt         # 依赖清单
├── md2wechat.yaml           # 全局配置 (自动生成)
├── themes/                  # 主题样式
│   ├── twilight.yaml
│   ├── chinese-scroll.yaml
│   └── brutalism.yaml
└── skill/md2wechat/scripts/ # 核心脚本
    ├── build.py             # 主程序 ⭐
    ├── python_converter.py  # Markdown 转 HTML
    ├── html_to_image.py     # HTML 截图
    └── ...
```

---

*Maintainer: @neo1_95*
