# md2wechat-skill 功能总结

## 🎉 项目概述

**md2wechat-skill** 是一个强大的多平台内容创作自动化工具，支持**微信公众号**和**小红书**双平台发布。

**GitHub 仓库**: https://github.com/beautifulboy9527/md2wechat-skill

---

## ✨ 核心功能清单

### 1. 📝 Markdown 转换引擎
- ✅ 智能 HTML 转换，完美适配微信和小红书
- ✅ 列表自动优化（悬挂缩进）
- ✅ 代码块卡片化渲染
- ✅ 引用块美化
- ✅ Table 包装技术（确保样式不丢失）

### 2. 🎨 多主题系统
- ✅ 7+ 内置主题
  - `default`: 简洁标准
  - `chinese-scroll`: 国风水墨
  - `fashion-bold`: 时尚高对比
  - `ocean-calm`: 商务理性
  - `autumn-warm`: 温暖治愈
  - `twilight`: 暗黑极客
  - `xhs-card`: **小红书专用** (3:4 比例)
- ✅ YAML 配置，易于扩展
- ✅ 支持自定义主题

### 3. 🖼️ AI 智能配图
- ✅ 自动封面生成
- ✅ 文内插图生成 (`__generate:prompt__`)
- ✅ 多尺寸支持 (16:9, 1:1, 9:16)
- ✅ 多引擎支持
  - ModelScope (通义万相)
  - OpenAI (DALL-E 3)
  - 兼容 Flux, Midjourney API 等
- ✅ 风格化生成 (tech, art, illustration 等)

### 4. 📕 小红书卡片模式 (NEW!)
- ✅ 3:4 完美比例 (1080x1440px)
- ✅ 渐变背景设计
- ✅ 自动分卡渲染
- ✅ 智能命名 (cover.png, card_1.png...)
- ✅ 配合 MCP 一键发布

### 5. ✍️ AI 写作助手 (NEW!)
- ✅ 产品经理 Persona
  - 第一人称叙述
  - 实战导向
  - 场景化写作
- ✅ 技术专家 Persona
  - 通俗易懂
  - 严谨准确
  - 代码友好
- ✅ 自动生成草稿
- ✅ 内置结构图生成 (Graphic Recording 风格)

### 6. 🚀 一键发布
- ✅ 微信公众号草稿箱 API
- ✅ 小红书 MCP 浏览器自动化
- ✅ 图片自动上传
- ✅ 批量处理支持

### 7. 🔧 高级功能
- ✅ Frontmatter 配置
- ✅ 自动图片压缩
- ✅ HTML 可视化渲染
- ✅ Mermaid 图表支持
- ✅ 手绘风格结构图
- ✅ 卡片式 Prompt 展示

---

## 🆚 核心优势

### vs 传统编辑器
| 特性 | md2wechat | 传统编辑器 |
|------|-----------|-----------|
| **写作体验** | Markdown 原生 | 富文本编辑器 |
| **版本控制** | ✅ Git 友好 | ❌ 不支持 |
| **自动化** | ✅ 一键生成 | ❌ 手动调整 |
| **AI 集成** | ✅ 深度集成 | ❌ 无 |
| **多平台** | ✅ 微信+小红书 | ❌ 单平台 |

### vs 其他工具
| 特性 | md2wechat | Auto-Redbook | 其他 Markdown 工具 |
|------|-----------|--------------|------------------|
| **平台支持** | 微信+小红书 | 仅小红书 | 仅微信 |
| **发布方式** | API + MCP | Cookie | 手动复制 |
| **稳定性** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **AI 生图** | ✅ | ❌ | ❌ |
| **主题系统** | ✅ 7+ 主题 | ❌ | ✅ 有限 |
| **写作助手** | ✅ | ❌ | ❌ |

---

## 🎯 典型使用场景

### 场景 1: 微信公众号技术文章
```bash
# 1. 创建草稿
python skill/writer/create_draft.py "AI大模型原理" --type tech

# 2. 编辑 Markdown
# (AI 会自动填充结构)

# 3. 生成并发布
python skill/md2wechat/scripts/build.py article.md --upload
```

### 场景 2: 小红书产品分享
```bash
# 1. 创建草稿
python skill/writer/create_draft.py "5个效率神器" --type pm

# 2. 编辑 Markdown (使用 --- 分隔卡片)

# 3. 生成卡片
python skill/md2wechat/scripts/build.py article.md --platform xhs --mode image

# 4. 发布到小红书
python ../xiaohongshu-publisher-skill/publish.py \
  --title "标题" \
  --content "描述" \
  --images cover.png card_1.png card_2.png
```

### 场景 3: 双平台同时发布
```bash
# 微信版本
python skill/md2wechat/scripts/build.py article.md --platform wechat --upload

# 小红书版本
python skill/md2wechat/scripts/build.py article.md --platform xhs --mode image
```

---

## 🔒 安全特性

### 配置安全
- ✅ 所有密钥存储在 `md2wechat.yaml`
- ✅ `.gitignore` 自动排除敏感文件
- ✅ 支持环境变量配置
- ✅ 示例文件不含真实密钥

### 文件安全
- ✅ 自动排除测试文件
- ✅ 自动排除日志文件
- ✅ 自动排除临时文件
- ✅ 仅保留必要的示例资源

---

## 📊 技术架构

### 核心模块
```
md2wechat-skill/
├── skill/md2wechat/        # 核心转换引擎
│   ├── python_converter.py # Markdown → HTML
│   ├── generate_image.py   # AI 图片生成
│   ├── wechat_uploader.py  # 微信 API
│   └── build.py            # 主构建脚本
├── skill/writer/           # AI 写作助手
│   ├── prompts.py          # Prompt 库
│   └── create_draft.py     # 草稿生成器
└── themes/                 # 主题系统
    ├── default.yaml
    ├── xhs-card.yaml
    └── ...
```

### 技术栈
- **语言**: Python 3.8+
- **核心库**:
  - `markdown`: Markdown 解析
  - `BeautifulSoup4`: HTML 处理
  - `css_inline`: CSS 内联
  - `playwright`: 浏览器渲染
  - `requests`: API 调用
  - `PyYAML`: 配置管理

---

## 🚀 未来规划

### 短期计划
- [ ] 封面图模板系统
- [ ] 标签自动提取
- [ ] 批量处理优化
- [ ] 更多主题

### 长期计划
- [ ] 支持更多平台 (知乎、CSDN)
- [ ] Web UI 界面
- [ ] 云端部署版本
- [ ] 协作编辑功能

---

## 📈 项目统计

- **代码行数**: ~3000+ lines
- **主题数量**: 7+
- **支持平台**: 2 (微信、小红书)
- **AI 引擎**: 3+ (ModelScope, OpenAI, 兼容)
- **文档完整度**: ⭐⭐⭐⭐⭐

---

## 🎊 总结

**md2wechat-skill** 是一个功能完整、架构清晰、安全可靠的多平台内容创作工具。

**核心亮点**:
1. ✅ **双平台支持**: 一套代码，微信+小红书
2. ✅ **AI 深度集成**: 自动配图 + 写作助手
3. ✅ **主题丰富**: 7+ 专业主题
4. ✅ **安全可靠**: 完善的隐私保护
5. ✅ **易于扩展**: 模块化设计

**适用人群**:
- 📝 内容创作者
- 🤖 AI Agent 开发者
- 💼 自媒体运营者
- 👨‍💻 技术博主

**立即开始**: https://github.com/beautifulboy9527/md2wechat-skill

---

<div align="center">

**Made with ❤️ for Creators**

</div>
