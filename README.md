# md2wechat Skill

<div align="center">

**优雅的公众号自动化写作助手**

[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

</div>

**md2wechat** 让公众号写作回归本质。使用 Markdown 撰写内容，自动完成排版、配图与上传，像发朋友圈一样简单。

---

## ✨ 核心功能

*   **📝 智能排版**: 自动将 Markdown 转换为微信兼容的 HTML，完美处理列表、代码块与引用。
*   **🎨 多样主题**: 内置 `chinese-scroll` (国风), `ocean-calm` (商务), `fashion-bold` (潮流) 等多款设计师级主题。
*   **🖼️ AI 自动配图**: 
    *   **智能封面**: 根据文章内容自动生成高质量封面图。
    *   **插图生成**: 支持 `![alt](__generate:描述__)` 语法，文章配图一键搞定。
*   **🃏 卡片式代码块**: 自动识别 Prompt/代码块，渲染为精美的卡片样式，提升阅读体验。
*   **📱 微信原生优化**: 
    *   自动将列表转换为悬挂缩进段落，适配微信阅读习惯。
    *   Table 包装技术，确保背景色与边框在微信中不丢失。
*   **🚀 一键发布**: 直接对接微信草稿箱接口，支持上传图片与文章。

## 🛠️ 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置

在项目根目录创建 `md2wechat.yaml` (已在 .gitignore 中排除，保障隐私):

```yaml
app_id: "你的微信AppID"
app_secret: "你的微信AppSecret"
image_key: "你的AI绘图Key" # 可选
```

### 3. 使用

撰写 Markdown 文件 (支持 Frontmatter 配置主题):

```markdown
---
theme: chinese-scroll
cover:
  prompt: "一只在写代码的猫"
---

# 我的文章标题

正文内容...
```

**生成并上传:**

```bash
python skill/md2wechat/scripts/build.py article.md --upload
```

## 🎨 主题列表

只需在 Markdown 头部指定 `theme` 字段即可切换：

*   `default`: 简洁标准
*   `chinese-scroll`: 国风水墨
*   `fashion-bold`: 时尚高对比
*   `ocean-calm`: 商务理性
*   `autumn-warm`: 温暖治愈
*   `twilight`: 暗黑极客

## 🔒 隐私说明

本项目严格遵守隐私安全原则：
*   所有敏感配置 (API Keys, Secrets) 均存储于 `md2wechat.yaml`。
*   `.gitignore` 已默认排除该配置文件及所有生成过程中的临时文件。
*   不会上传任何个人数据至 Git 仓库。

---
<div align="center">
Made with ❤️ for Creators
</div>
