---
name: doubao-image-gen
description: 豆包（Doubao）网页版 AI 图像生成。触发词："掉豆包"、"调用豆包"、"豆包生图"、"豆包生成"、"用豆包生成图片"。用户上传参考图片 + 给出提示词 + 说触发词时自动执行：在豆包网页版上传参考图、输入提示词、生成并截图返回。依赖 browser-use skill 控制 Chrome 浏览器。
---

# 豆包图像生成

## 触发条件

同时满足以下 3 个条件时触发：
1. 用户提供了参考图片（上传附件 或 指定本地路径）
2. 用户给出了生成提示词
3. 用户使用了触发词：**"掉豆包"** / **"调用豆包"** / **"豆包生图"** / **"豆包生成"** / **"用豆包生成"**

## 依赖

- **browser-use skill**：已安装（browser-use 0.13.0），用于控制 Chrome
- Chrome 需已启动远程调试（CDP 端口 9222），且**已登录豆包账号**

## 执行流程

### 1. 确认输入

从用户消息中提取：
- **图片路径**：用户上传的图片保存路径，或明确指定的本地路径
- **提示词**：用户指定的生成提示文本

### 2. 环境检查

```bash
browser-use doctor
```

确认 browser-use 可用、Chrome CDP 可连接。

### 3. 连接 Chrome 并打开豆包

```bash
browser-use connect
browser-use --headed open https://www.doubao.com/chat/
```

等待 3 秒页面加载，snapshot 确认。

### 4. 进入图像生成模式

snapshot 找到"图像生成"按钮 → click。再次 snapshot 确认进入图像生成界面（应有文件上传 input 和文本输入框）。

如果页面跳回对话界面，重新点击"图像生成"。

### 5. 上传参考图片

snapshot 找到 `input[type=file]` 元素（通常隐藏在"加号/上传"按钮后）。

**逐张上传**，每张确认预览 img 出现后再上传下一张：

```bash
browser-use --headed act <file_input_id> upload "<图片路径>"
```

### 6. 输入提示词

snapshot 找到文本输入框（textarea / contenteditable div）。

**先清空**（可能残留上次对话文本），再输入提示词：

```bash
browser-use --headed act <input_id> type "<提示词>"
```

### 7. 提交生成

snapshot 找到发送按钮（通常标有 SVG 箭头图标）→ click。

### 8. 等待并截图

等待 15-30 秒生成完成。periodically snapshot 检查进度。

生成完成后截图保存：

```bash
browser-use --headed screenshot C:\Users\Administrator\.qclaw\workspace\doubao_result.png
```

## 注意事项

- 上传图片需**逐张进行**，确认预览后再下一张
- 输入框可能残留文本，**必须先清空再输入**
- 页面可能跳回对话界面，需反复确认在图像生成模式
- 生成时间 15-60 秒，取决于图片数量和复杂度
- 结果截图保存到 workspace 目录