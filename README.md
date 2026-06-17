# 🎨 Doubao Image Gen Skill

> 豆包（Doubao）网页版 AI 图像生成 Skill  
> 通过 **browser-use** 控制 Chrome 浏览器，自动上传参考图并生成 AI 图像

---

## ✨ 功能特性

- 🖼️ **自动上传参考图片** — 支持单张/多张参考图
- 🤖 **AI图像生成** — 在豆包网页版自动输入提示词并生成
- 📸 **截图返回结果** — 生成完成后自动截图保存
- 🔗 **无缝集成** — 触发词激活，全自动执行流程

## 🚀 触发方式

同时满足以下 **3 个条件**时触发：

| 条件 | 说明 | 示例 |
|------|------|------|
| 1️⃣ 提供参考图片 | 上传附件或指定本地路径 | `C:\Users\Administrator\Downloads\ref.png` |
| 2️⃣ 给出提示词 | 指定生成提示文本 | `"赛博朋克风格的未来城市"` |
| 3️⃣ 使用触发词 | 必须包含以下任一关键词 | `"掉豆包"` / `"调用豆包"` / `"豆包生图"` / `"豆包生成"` / `"用豆包生成"` |

### 使用示例

```
用户：[上传图片] + "帮我生成一个赛博朋克风格的未来城市，掉豆包"
用户："用 C:\Users\Administrator\Downloads\ref.png 作为参考，生成一只机械猫，调用豆包"
```

---

## 📋 系统依赖

### 必需组件

| 组件 | 版本要求 | 用途 |
|------|---------|------|
| **Chrome 浏览器** | 最新版 | 运行豆包网页版 |
| **browser-use** | ≥0.13.0 | 控制浏览器自动化 |
| **Python 3.8+** | — | 运行环境检查脚本 |

### Chrome 启动要求

Chrome 需以 **远程调试模式**启动：

```bash
# Windows PowerShell
Start-Process chrome.exe -ArgumentList "--remote-debugging-port=9222"

# 或使用完整用户数据目录（保留登录态）
Start-Process chrome.exe -ArgumentList "--remote-debugging-port=9222 --user-data-dir=`"C:\Users\Administrator\AppData\Local\Google\Chrome\User Data`""
```

> ⚠️ **重要：** 必须在启动前关闭所有 Chrome 窗口，否则端口冲突！

### 安装 browser-use

```bash
pip install browser-use>=0.13.0
```

---

## 🔧 实现步骤（完整执行流程）

### 步骤 1：确认输入参数

从用户消息中提取：
- **图片路径** — 用户上传的附件路径或明确指定的本地文件路径
- **提示词** — 用户指定的 AI 生成提示文本

**验证检查：**
```powershell
# 确认图片文件存在
Test-Path $imagePath

# 确认提示词非空
if (-not $prompt) { Write-Error "请提供生成提示词" }
```

---

### 步骤 2：环境检查

运行环境诊断脚本，确认所有依赖就绪：

```bash
python scripts/env_check.py
```

**预期输出：**
```
=== 豆包图像生成 - 环境检查 ===

[OK] browser-use is ready
[OK] Chrome connected via CDP

[READY] 环境就绪，可以开始豆包图像生成流程。
```

**如果失败：**
- `browser-use check failed` → 执行 `pip install browser-use`
- `Cannot connect to Chrome` → 确认 Chrome 以远程调试模式启动（端口 9222）

---

### 步骤 3：连接浏览器并打开豆包

```bash
# 连接到已运行的 Chrome 实例
browser-use connect

# 打开豆包网页版（已登录状态）
browser-use --headed open https://www.doubao.com/chat/
```

**等待页面加载完成：**
```bash
browser-use --headed wait --load networkidle
```

> ⚠️ 确保 Chrome 已登录豆包账号！首次使用需手动登录一次。

---

### 步骤 4：进入图像生成模式

```bash
# 获取页面快照，找到交互元素
browser-use --headed snapshot -i
```

在快照中找到 **"图像生成"** 按钮（通常位于对话界面侧边栏或工具栏），然后点击：

```bash
browser-use --headed click @<图像生成按钮的ref>
```

**验证进入成功：**
```bash
# 再次快照确认界面变化
browser-use --headed snapshot -i
# 应该看到：文件上传 input 元素 + 文本输入框
```

**常见问题：**
- 如果页面跳回对话界面 → 重新点击 "图像生成" 按钮
- 如果找不到按钮 → 可能需要先在对话框中输入 `/image` 或类似命令

---

### 步骤 5：上传参考图片

**找到文件上传元素：**
```bash
browser-use --headed snapshot -i
# 寻找 input[type=file] 元素（通常隐藏在"加号"/"上传"/"📎"按钮后）
```

**逐张上传（重要！）：**

```bash
# 上传第一张参考图
browser-use --headed act <file_input_ref> upload "C:\path\to\image1.png"

# 等待预览出现后，再上传第二张
browser-use --headed act <file_input_ref> upload "C:\path\to\image2.png"
```

**每张图片上传后：**
```bash
# 等待预览图出现（通常1-3秒）
Start-Sleep -Seconds 2

# 快照确认预览 img 元素已显示
browser-use --headed snapshot -i
```

> ⚠️ **关键规则：** 必须**逐张上传、逐张确认**！不要批量一次性上传多张，否则可能只识别最后一张。

---

### 步骤 6：输入生成提示词

**找到文本输入框：**
```bash
browser-use --headed snapshot -i
# 寻找 textarea 或 contenteditable div（通常是底部的输入区域）
```

**清空残留文本（重要！）：**
```bash
# 先全选删除旧内容
browser-use --headed act <input_ref> key "Control+a"
browser-use --headed act <input_ref> key "Delete"
```

**输入新提示词：**
```bash
browser-use --headed act <input_ref> type "<你的提示词>"
```

**示例提示词：**
```
赛博朋克风格的城市夜景，霓虹灯闪烁，飞行汽车穿梭于高楼之间，雨后的街道反射着彩色光芒，电影级构图，8K超高清
```

---

### 步骤 7：提交生成请求

**找到发送按钮：**
```bash
browser-use --headed snapshot -i
# 通常是一个带箭头图标的 SVG 按钮（➤）
```

**点击发送：**
```bash
browser-use --headed click @<发送按钮ref>
```

---

### 步骤 8：等待生成完成

**轮询检查进度：**
```bash
# 每5秒检查一次状态
for ($i = 1; $i -le 12; $i++) {
    Write-Output "等待生成中... ($i/12)"
    Start-Sleep -Seconds 5
    
    # 快照检查是否已完成
    browser-use --headed snapshot -i
    # 如果看到生成的图片元素，跳出循环
}
```

**预计时间：**
| 图片数量 | 复杂度 | 预计耗时 |
|---------|--------|---------|
| 1张参考图 | 简单提示词 | 15-30秒 |
| 1张参考图 | 复杂提示词 | 30-60秒 |
| 多张参考图 | 任意 | 45-90秒 |

---

### 步骤 9：截图保存结果

```bash
# 截图保存到 workspace 目录
browser-use --headed screenshot "C:\Users\Administrator\.qclaw\workspace\doubao_result.png"
```

**可选：同时保存到用户指定路径：**
```bash
browser-use --headed screenshot "C:\Users\Administrator\Downloads\doubao_output_$(Get-Date -Format 'yyyyMMdd_HHmmss').png"
```

---

## 📁 文件结构

```
doubao-image-gen-skill/
├── SKILL.md              # Skill 定义文件（Agent 读取）
├── README.md             # 本说明文档
└── scripts/
    └── env_check.py      # 环境检查辅助脚本
```

---

## ⚠️ 注意事项 & 常见问题

### ❗ 关键注意事项

| 问题 | 解决方案 |
|------|---------|
| **上传图片必须逐张进行** | 确认预览出现后再传下一张，否则只识别最后一张 |
| **输入框可能有残留文本** | 每次输入前必须先 `Ctrl+A` → `Delete` 清空 |
| **页面可能跳回对话界面** | 反复确认在"图像生成"模式，必要时重新点击进入 |
| **Chrome 必须远程调试模式** | 启动时加 `--remote-debugging-port=9222` |
| **必须已登录豆包账号** | 首次使用需手动登录，后续保持登录态 |

### 🔧 故障排查

**问题1：browser-use 连接失败**
```bash
# 检查 Chrome 是否运行且开启调试端口
curl http://localhost:9222/json/version

# 如果无响应，重启 Chrome
Stop-Process -Name chrome -Force -ErrorAction SilentlyContinue
Start-Process chrome.exe -ArgumentList "--remote-debugging-port=9222"
```

**问题2：页面加载超时**
```bash
# 增加超时时间
browser-use --headed open https://www.doubao.com/chat/ --timeout 30000

# 或手动等待
Start-Sleep -Seconds 5
browser-use --headed wait --load networkidle
```

**问题3：找不到"图像生成"按钮**
- 尝试在对话输入框输入 `/image` 或 `画图`
- 检查豆包版本更新后 UI 变化
- 截图发给我分析最新界面

**问题4：生成时间过长**
- 减少参考图片数量
- 简化提示词长度
- 检查网络连接稳定性

---

## 🔄 工作流程图

```
┌─────────────────────────────────────────────────────┐
│                    用户触发                          │
│  [参考图片] + [提示词] + ["掉豆包"/"调用豆包"]       │
└─────────────────────┬───────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────┐
│              步骤1: 解析输入参数                     │
│         提取图片路径 + 提示词文本                    │
└─────────────────────┬───────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────┐
│              步骤2: 环境检查                         │
│     python env_check.py → 确认 browser-use + Chrome │
└─────────────────────┬───────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────┐
│          步骤3: 打开豆包网页版                       │
│   browser-use connect → open doubao.com/chat        │
└─────────────────────┬───────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────┐
│         步骤4: 进入图像生成模式                      │
│            点击"图像生成"按钮                        │
└─────────────────────┬───────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────┐
│           步骤5: 上传参考图片                        │
│      逐张 upload → 确认预览 → 下一张                 │
└─────────────────────┬───────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────┐
│           步骤6: 输入提示词                          │
│         清空旧文本 → type 新提示词                   │
└─────────────────────┬───────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────┐
│           步骤7: 提交生成                            │
│              点击发送按钮 ➤                          │
└─────────────────────┬───────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────┐
│           步骤8: 等待生成完成                         │
│      轮询检查 (15-60秒) → 确认图片出现               │
└─────────────────────┬───────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────┐
│           步骤9: 截图保存结果                         │
│     screenshot → doubao_result.png                  │
└─────────────────────────────────────────────────────┘
                      ▼
                ✅ 完成！返回图片给用户
```

---

## 📄 License

MIT License — 自由使用、修改和分发。

## 👨‍💻 Author

Created for **QClaw Agent Workspace**  
Compatible with OpenClaw Skill System.

---

> 💡 **提示：** 此 Skill 依赖 `browser-use` 进行浏览器自动化，确保 Chrome 以远程调试模式启动且已登录豆包账号。