# md2wechat Skill

<div align="center">

**用 Markdown 写公众号文章，像发朋友圈一样简单**

[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Original Author](https://img.shields.io/badge/Original-geekjourney-orange)](https://github.com/geekjourney)

[快速开始](#-30-秒快速开始) • [功能介绍](#-功能一览) • [使用指南](#-使用指南) • [进阶配置](#-进阶配置)

---

</div>

## ✨ 这是什么？

**md2wechat** 是一个全流程的公众号自动化写作助手。它不仅仅是排版工具，更能帮你搞定配图、页脚甚至自动上传。

> 💡 **一句话理解**：Markdown 写作 → AI 自动配图 → 智能排版 → 自动发到微信草稿箱

**核心亮点：**
*   🎨 **智能排版**：支持卷轴、科技、极简等多种风格，自动适配 CSS。
*   🖼️ **AI 配图**：集成 ModelScope，根据文章内容自动生成封面和插图。
*   📸 **卡片模式**：**独家功能**！自动将文章按章节切分为高清卡片图片，完美还原设计稿，不受微信编辑器限制。
*   🦶 **动态页脚**：一键注入动态 SVG 分隔符、二维码和往期推荐。
*   🚀 **自动发布**：直接上传图片和草稿到微信公众号后台。

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

### 方式三：卡片长图模式 (Card Mode)
适合制作精美的海报式文章，或者当你想完全掌控排版细节时。
脚本会自动将文章按章节（H1/H2）切分为多张 **1080px 宽的高清卡片**，并自动拼接。

```bash
python skill/md2wechat/scripts/build.py my_article.md --mode image --upload
```

**效果特点：**
*   ✅ **高清无损**：3倍超采样渲染，文字锐利清晰。
*   ✅ **卡片设计**：自动添加圆角、阴影和舒适的边距，像精心设计的 PPT。
*   ✅ **完美还原**：彻底解决微信编辑器“吃样式”的问题。

---

## ⚙️ 进阶配置

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

## 🙏 致谢

本项目基于 [geekjourney/md2wechat-skill](https://github.com/geekjourney) 开发，感谢原作者的开源贡献。
我们在原版基础上进行了 Python 重构，并增加了 AI 生图、卡片模式和自动上传等新功能。

---

*Maintainer: @neo1_95*
