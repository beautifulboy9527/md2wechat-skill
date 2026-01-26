# md2wechat Skill

<div align="center">

**优雅的多平台自动化写作助手**

[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-WeChat%20%7C%20Xiaohongshu-orange)](https://github.com)

</div>

**md2wechat** 让内容创作回归本质。使用 Markdown 撰写内容，自动完成排版、配图与发布，支持**微信公众号**和**小红书**双平台。

---

## ✨ 核心功能

### 📝 智能排版
- **Markdown 转换**: 自动转换为平台兼容的 HTML，完美处理列表、代码块与引用
- **多样主题**: 内置 7+ 设计师级主题，一键切换风格
- **微信优化**: 列表悬挂缩进、Table包装技术，确保样式不丢失

### 🎨 AI 智能配图
- **智能封面**: 根据文章内容自动生成高质量封面图
- **插图生成**: 支持 `![alt](__generate:描述|size=16:9__)` 语法
- **多引擎支持**: ModelScope、OpenAI、DALL-E、Flux 等

### 🃏 增强功能
- **卡片式代码块**: 自动识别 Prompt/代码块，渲染为精美卡片
- **结构化图表**: 支持手绘风格的内容结构图 (Graphic Recording)
- **AI 写作助手**: 内置产品经理和技术专家写作 Persona

### 📕 小红书卡片模式 (NEW!)
- **3:4 完美比例**: 1080x1440px 专为小红书优化
- **渐变背景**: 粉紫蓝渐变，吸引眼球
- **自动分卡**: 按 `---` 分隔符自动生成多张卡片
- **一键发布**: 配合 `xiaohongshu-publisher-skill` 直接发布

### 🚀 一键发布
- **微信草稿箱**: 直接上传到微信公众号草稿箱
- **小红书发布**: 生成卡片后可通过 MCP 发布
- **批量处理**: 支持同时生成多平台版本

---

## 🛠️ 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置

在项目根目录创建 `md2wechat.yaml` (参考 `md2wechat.example.yaml`):

```yaml
# 微信公众号配置 (必需)
app_id: "your_wechat_app_id"
app_secret: "your_wechat_app_secret"

# AI 生图配置 (可选)
# 方式 A: 使用 ModelScope (默认)
image_provider: "modelscope"
image_key: "your_modelscope_api_key"
image_model: "Tongyi-MAI/Z-Image-Turbo"

# 方式 B: 使用 OpenAI 兼容接口
# image_provider: "openai"
# image_api_base: "https://api.openai.com/v1"
# image_key: "sk-..."
# image_model: "dall-e-3"
```

### 3. 使用示例

#### 微信公众号

撰写 Markdown 文件:

```markdown
---
theme: chinese-scroll
cover:
  prompt: "一只在写代码的猫"
---

# 我的文章标题

正文内容...

![配图](__generate:futuristic city, cyberpunk style|size=16:9__)
```

**生成并上传:**

```bash
python skill/md2wechat/scripts/build.py article.md --upload
```

#### 小红书卡片

撰写 Markdown 文件:

```markdown
---
title: 5个让效率翻倍的AI工具
theme: xhs-card
---

# 🚀 主标题
引言内容...

---

## 1️⃣ 第一个工具
介绍内容...

---

## 2️⃣ 第二个工具
介绍内容...

---

#AI工具 #效率提升 #小红书
```

**生成卡片:**

```bash
python skill/md2wechat/scripts/build.py article.md --platform xhs --mode image
```

**发布到小红书:**

```bash
python ../xiaohongshu-publisher-skill/publish.py \
  --title "标题（不超过20字）" \
  --content "描述内容" \
  --images cover.png card_1.png card_2.png
```

---

## 🎨 主题列表

只需在 Markdown 头部指定 `theme` 字段即可切换：

| 主题名称 | 风格描述 | 适用场景 |
|---------|---------|---------|
| `default` | 简洁标准 | 通用文章 |
| `chinese-scroll` | 国风水墨 | 传统文化、诗词 |
| `fashion-bold` | 时尚高对比 | 潮流、设计 |
| `ocean-calm` | 商务理性 | 职场、技术 |
| `autumn-warm` | 温暖治愈 | 生活、情感 |
| `twilight` | 暗黑极客 | 科技、编程 |
| `xhs-card` | **小红书专用** | 3:4卡片，渐变背景 |

---

## 📖 高级功能

### AI 写作助手

使用内置的写作 Persona 快速生成文章草稿：

```bash
# 产品经理风格
python skill/writer/create_draft.py "DeepSeek vs ChatGPT" --type pm

# 技术专家风格
python skill/writer/create_draft.py "AI大模型原理" --type tech
```

生成的草稿包含：
- 结构化大纲
- AI 生成的封面图和结构图
- 写作指导 Prompt

### 图片生成语法

支持多种图片生成方式：

```markdown
# 基础生成
![描述](__generate:prompt__)

# 指定尺寸
![描述](__generate:prompt|size=16:9__)

# 指定风格
![描述](__generate:prompt|style=tech|sub_style=sci_fi__)

# 手绘结构图
![结构图](__generate:mind map of AI tools|style=graphic_recording__)
```

### 平台对比

| 特性 | 微信公众号 | 小红书 |
|------|-----------|--------|
| **输出格式** | HTML | PNG 卡片 |
| **尺寸** | 自适应 | 1080x1440 (3:4) |
| **主题** | 所有主题 | `xhs-card` 推荐 |
| **发布方式** | API 直传 | MCP 浏览器自动化 |
| **命令** | `--platform wechat` | `--platform xhs --mode image` |

---

## 🔒 隐私与安全

本项目严格遵守隐私安全原则：

- ✅ 所有敏感配置 (API Keys, Secrets) 均存储于 `md2wechat.yaml`
- ✅ `.gitignore` 已默认排除配置文件及临时文件
- ✅ 不会上传任何个人数据至 Git 仓库
- ✅ 支持本地运行，无需联网（除 AI 生图）

**重要提醒:**
- 请勿将 `md2wechat.yaml` 提交到版本控制
- 定期更换 API 密钥
- 使用环境变量管理敏感信息

---

## 📂 项目结构

```
md2wechat-skill/
├── skill/
│   ├── md2wechat/
│   │   └── scripts/
│   │       ├── build.py              # 主构建脚本
│   │       ├── python_converter.py   # Markdown 转换器
│   │       ├── generate_image.py     # AI 图片生成
│   │       └── wechat_uploader.py    # 微信上传
│   └── writer/
│       ├── prompts.py                # 写作 Prompt 库
│       └── create_draft.py           # 草稿生成器
├── themes/
│   ├── default.yaml
│   ├── chinese-scroll.yaml
│   ├── xhs-card.yaml                 # 小红书主题
│   └── ...
├── examples/
│   ├── basic_example.md
│   └── xhs_example.md                # 小红书示例
├── SKILL.md                          # AI Agent 使用文档
└── README.md                         # 本文档
```

---

## 🎯 核心优势

### vs 传统编辑器
- ✅ **Markdown 原生**: 无需学习复杂编辑器
- ✅ **版本控制**: Git 友好，支持协作
- ✅ **自动化**: 一键生成，无需手动调整

### vs 其他工具
- ✅ **双平台支持**: 微信 + 小红书，一套代码
- ✅ **AI 深度集成**: 自动配图、写作助手
- ✅ **MCP 标准**: 可被 AI Agent 调用

### vs Auto-Redbook-Skills
- ✅ **更稳定**: MCP 浏览器自动化 vs Cookie 方式
- ✅ **功能更强**: 支持 AI 生图、多主题、双平台
- ✅ **架构统一**: 集成到现有系统，无需额外维护

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

**开发建议:**
1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 🙌 致谢

本项目基于 [geekjourneyx/md2wechat-skill](https://github.com/geekjourneyx/md2wechat-skill) 二次开发。感谢原作者的创意与贡献！

我们在此基础上进行了 Python 重构，增强了本地化处理能力与 AI 生图集成，并新增了小红书卡片模式，使其更适合自动化 Agent 使用。

**特别感谢:**
- [BND-1/wechat_article_skills](https://github.com/BND-1/wechat_article_skills) - 写作 Persona 灵感来源
- [comeonzhj/Auto-Redbook-Skills](https://github.com/comeonzhj/Auto-Redbook-Skills) - 小红书卡片渲染参考

---

## 📄 License

MIT License - 详见 [LICENSE](LICENSE) 文件

---

<div align="center">

**Made with ❤️ for Creators**

如果这个项目对你有帮助，欢迎 ⭐ Star 支持！

</div>
