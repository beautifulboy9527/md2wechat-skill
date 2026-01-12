# 图片语法说明

## 图片引用类型

在 Markdown 中，支持三种图片引用方式：

### 1. 本地图片

```markdown
![图片描述](./path/to/image.png)
![图片描述](/absolute/path/image.jpg)
![图片描述](../images/photo.gif)
```

**处理流程**：
1. 读取本地文件
2. 压缩（如果宽度 > 1920px）
3. 上传到微信素材库
4. 替换为微信 CDN URL

**支持的格式**：JPG, PNG, GIF

### 2. 在线图片

```markdown
![图片描述](https://example.com/image.jpg)
![图片描述](http://example.com/image.png)
```

**处理流程**：
1. 下载图片到临时目录
2. 压缩（如果宽度 > 1920px）
3. 上传到微信素材库
4. 替换为微信 CDN URL

**注意**：必须确保图片可访问，且格式正确

### 3. AI 生成图片

```markdown
![图片描述](__generate:A cute cat sitting on a windowsill__)
```

**语法**：`![alt](__generate:prompt__)`

- `__generate:` 是固定前缀
- `prompt` 是图片生成提示词
- 支持中英文提示词

**处理流程**：
1. 提取 prompt 内容
2. 调用图片生成 API
3. 获取生成的图片 URL
4. 下载图片
5. 上传到微信素材库
6. 替换为微信 CDN URL

**配置要求**：
- `IMAGE_API_KEY`: 图片 API 密钥
- `IMAGE_API_BASE`: 图片 API 基础 URL

## 图片占位符

在生成 HTML 时，使用占位符标记图片位置：

```html
<!-- IMG:0 -->
<!-- IMG:1 -->
<!-- IMG:2 -->
```

索引从 0 开始，按图片在 Markdown 中出现的顺序编号。

## 图片处理命令

### 上传本地图片

```bash
bash scripts/run.sh upload_image "/path/to/image.png"
```

**响应**：
```json
{
  "success": true,
  "wechat_url": "https://mmbiz.qpic.cn/mmbiz_jpg/xxx/0?wx_fmt=jpeg",
  "media_id": "media_id_xxx",
  "width": 1920,
  "height": 1080
}
```

### 下载并上传在线图片

```bash
bash scripts/run.sh download_and_upload "https://example.com/image.jpg"
```

**响应**：同上

### AI 生成图片

```bash
bash scripts/run.sh generate_image "A futuristic city skyline at sunset with flying cars and neon lights"
```

**响应**：
```json
{
  "success": true,
  "prompt": "A futuristic city...",
  "original_url": "https://image-api.example.com/generated/xxx.jpg",
  "wechat_url": "https://mmbiz.qpic.cn/mmbiz_jpg/xxx/0?wx_fmt=jpeg",
  "media_id": "media_id_xxx",
  "width": 1024,
  "height": 1024
}
```

## 图片压缩规则

| 条件 | 处理方式 |
|------|----------|
| 宽度 > 1920px | 等比缩放至 1920px |
| 文件大小 > 2MB | 压缩质量 |
| 格式不支持 | 转换为 JPG |

## 错误处理

| 错误 | 处理方式 |
|------|----------|
| 本地文件不存在 | 返回错误，跳过该图片 |
| 在线图片下载失败 | 返回错误，跳过该图片 |
| AI 生成失败 | 返回错误，跳过该图片 |
| 微信上传失败 | 返回错误，跳过该图片 |
| 图片格式不支持 | 尝试转换，失败则跳过 |

## 示例

### 示例 1：纯本地图片

```markdown
# 巴黎旅行日记

## 第一天：埃菲尔铁塔

终于来到了梦寐以求的巴黎！

![埃菲尔铁塔](./photos/eiffel.jpg)

傍晚的铁塔格外美丽...
```

**处理**：
1. 检测到 1 张本地图片
2. 上传 `./photos/eiffel.jpg`
3. HTML 中使用 `<!-- IMG:0 -->` 占位
4. 替换为微信 URL

### 示例 2：混合类型

```markdown
# 科技产品评测

## 产品外观

![产品图](https://example.com/product.jpg)

## 概念设计

![未来概念](__generate:Futuristic gadget design with glowing blue lights, minimalist style__)

## 规格参数

详见下表：
```

**处理**：
1. 检测到 2 张图片（1 张在线，1 张 AI 生成）
2. 处理在线图片
3. 处理 AI 生成图片
4. 按顺序替换占位符

### 示例 3：AI 生成多图

```markdown
# 未来城市系列

## 概念图 1

![概念图1](__generate:Futuristic city with vertical gardens and flying vehicles__)

## 概念图 2

![概念图2](__generate:Underwater city with bio-luminescent buildings__)

## 概念图 3

![概念图3](__generate:Space station with rotating gravity ring and Earth view__)
```

**处理**：
1. 检测到 3 张 AI 生成图片
2. 依次调用图片生成 API
3. 每张图片独立上传到微信
4. 按顺序替换占位符
