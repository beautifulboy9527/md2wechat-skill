# md2wechat Skill (Enhanced)

<div align="center">

**用 Markdown 写公众号文章，像发朋友圈一样简单**

[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Maintainer](https://img.shields.io/badge/Maintainer-neo1__95-blue)](https://github.com/neo1_95)
[![X Follow](https://img.shields.io/twitter/follow/neo1_95?style=social)](https://x.com/neo1_95)

[快速开始](#-30-秒快速开始) • [功能介绍](#-功能一览) • [详细指南](#-详细使用指南) • [主题展示](#-主题与风格) • [常见问题](#-常见问题)

---

</div>

## ✨ 项目简介

**md2wechat** 是一个全流程的公众号自动化写作助手。
本项目在原版 [geekjourneyx/md2wechat-skill](https://github.com/geekjourneyx/md2wechat-skill) 的基础上进行了**深度重构与功能增强**。

> 💡 **一句话理解**：Markdown 写作 → AI 自动配图 → 智能排版 → 自动发到微信草稿箱

**🚀 新增核心亮点 (相比原版)：**
*   **📸 独家卡片模式**：将文章自动切分为高清长图/卡片，完美还原设计稿，彻底解决微信后台“吃样式”问题。
*   **🖼️ AI 深度集成**：支持 Claude/ModelScope 双引擎，根据上下文自动生成高质量配图。
*   **🎨 更多精美主题**：新增 Fashion-Bold, Chinese-Scroll 等 8+ 款设计师级主题。
*   **🛠️ 体验优化**：重写了 CLI 交互，支持 Windows/Mac 一键运行，无需复杂配置。

---

## 🚀 30 秒快速开始

**小白用户只需 3 步：**

### 1. 安装与配置

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

### 2. 开始写作

创建一个 `article.md` 文件：

```markdown
---
theme: chinese-scroll
cover:
  prompt: "一只在写代码的猫"
---

# 我的第一篇文章

这里是正文内容...
```

### 3. 生成与预览

```bash
# 仅预览 HTML
python skill/md2wechat/scripts/build.py article.md

# 生成并上传到微信草稿箱
python skill/md2wechat/scripts/build.py article.md --upload
```

打开生成的 `article_wechat.html` 即可预览效果！

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

## 📖 详细使用指南

### 1. Markdown 结构与资源

脚本会自动解析 Markdown 中的以下元素：

*   **标题**：自动提取第一个 `# 标题` 作为文章标题。
*   **摘要**：自动提取第一段作为摘要（或在 Frontmatter 中指定）。
*   **图片**：
    *   **本地图片**：`![alt](./img/photo.jpg)` -> 自动上传到微信服务器。
    *   **在线图片**：`![alt](https://...)` -> 自动下载并上传。
    *   **AI 生图**：`![alt](__generate:详细的画面描述__)` -> 自动调用 AI 生成并上传。

### 2. 转换模式 (Mode)

| 模式 | 命令参数 | 适用场景 | 特点 |
|------|----------|----------|------|
| **文本模式** | 默认 | 常规文章 | 生成 HTML，保留文字可复制性，适合大多数文章。 |
| **卡片模式** | `--mode image` | 海报、长图 | 将每一章节渲染为一张高清图片，拼接成长图。视觉效果最强，但文字不可复制。 |

**卡片模式示例：**
```bash
python skill/md2wechat/scripts/build.py my_article.md --mode image --upload
```

### 3. 配置文件详解

支持在项目根目录 `md2wechat.yaml` 或 Markdown 文件的 Frontmatter 中配置。

**Frontmatter (优先级最高):**
```yaml
---
theme: twilight                 # 主题
title: 自定义标题                # 覆盖默认标题
digest: 这是摘要                # 覆盖默认摘要
cover:
  prompt: "赛博朋克风格的城市"    # 封面提示词
  style: sci_fi                 # 封面风格
footer:
  type: qr
  qr_image: "assets/qr.jpg"
---
```

**全局配置 (`md2wechat.yaml`):**
```yaml
# 微信公众号配置 (必须)
app_id: "wx-xxxxxxxx"
app_secret: "xxxxxxxx"

# AI 绘图配置 (可选)
image_key: "sk-xxxx"
image_api_base: "https://..."

# 默认页脚配置
footer:
  template: glass_contact
  title: "关注我"
```

---

## 🎨 主题与风格

我们内置了多种精心设计的主题，满足不同场景需求：

| 主题名称 (`theme`) | 风格描述 | 适用场景 |
|-------------------|----------|----------|
| **default** | 简洁、专业、标准 | 通用、技术文档 |
| **chinese-scroll** | **国风、卷轴、水墨** | 文化、历史、散文 |
| **fashion-bold** | **时尚、大胆、高对比** | 潮流、设计、艺术 |
| **brutalism** | **新丑主义、高饱和、黑白** | 独立观点、先锋艺术 |
| **twilight** | **暗黑模式、霓虹、极客** | 科技新闻、夜读 |
| **autumn-warm** | 温暖、橙色调、治愈 | 情感、生活方式 |
| **spring-fresh** | 清新、绿色、自然 | 户外、健康、旅行 |
| **ocean-calm** | 冷静、蓝色、理性 | 商业分析、深度报道 |

**如何预览主题？**
只需修改 Markdown 头部的 `theme` 字段，重新运行脚本即可。

---

## ❓ 常见问题 (Troubleshooting)

### 配置问题
**Q: 提示 `AppID not configured`？**
A: 请确保 `md2wechat.yaml` 文件存在且填入了正确的 `app_id` 和 `app_secret`。或者在命令前设置环境变量：
`set WECHAT_APPID=your_id` (Windows) / `export WECHAT_APPID=your_id` (Mac/Linux)

### 图片问题
**Q: 图片上传失败？**
A: 微信接口对图片大小有限制（通常 < 10MB）。脚本会自动压缩图片，但如果图片过大或格式不支持（如 WebP），可能会失败。建议使用 JPG/PNG。

**Q: AI 生图失败？**
A: 请检查 `image_key` 是否正确，以及您的账户是否有余额。

### 微信接口问题
**Q: 报错 `IP not in whitelist`？**
A: 微信公众号开发需要配置 IP 白名单。
1. 访问 [ip.sb](https://ip.sb) 查看本机公网 IP。
2. 登录微信公众号后台 -> 设置与开发 -> 基本配置 -> IP白名单 -> 修改并添加您的 IP。

**Q: 报错 `create draft failed`？**
A: 可能原因：
1. 账号未认证（部分接口受限）。
2. 文章内容包含敏感词。
3. 草稿箱已满。

---

## 👨‍💻 作者与维护

**当前维护者 (Maintainer):**

*   **一辉 (@neo1_95)**
    *   X (Twitter): [@neo1_95](https://x.com/neo1_95)
    *   GitHub: [neo1_95](https://github.com/neo1_95)
    *   *欢迎关注我的 X 账号，获取更多 AI 提效工具与开发心得。*

**致谢 (Credits):**

*   本项目 Fork 并改进自 [geekjourneyx/md2wechat-skill](https://github.com/geekjourneyx/md2wechat-skill)。
*   感谢原作者的创意与开源贡献，为本项目提供了坚实的基础。

---
