# 🔐 API Key 配置指南

## 📋 概述

Manus AI 代理系统需要配置 API Key 才能使用完整的 AI 功能。本指南将帮助您配置所需的 API Key。

## 🚀 快速开始

### 1. 创建环境变量文件

在项目根目录下创建 `.env` 文件：

**Windows (PowerShell):**
```powershell
cd manus-ai-system
Copy-Item .env.example .env
```

**Linux/Mac:**
```bash
cd manus-ai-system
cp .env.example .env
```

### 2. 编辑环境变量文件

使用文本编辑器打开 `.env` 文件，填入您的 API Key。

## 🔑 必需的 API Key

### OpenAI API Key（必需）

**用途：**
- 规划智能体：任务分解与执行规划
- 代码智能体：代码生成与执行
- GUI智能体：屏幕理解与操作决策（使用视觉模型）
- 评估智能体：任务完成度评估

**获取方式：**
1. 访问 [OpenAI Platform](https://platform.openai.com/)
2. 注册/登录账户
3. 进入 [API Keys 页面](https://platform.openai.com/api-keys)
4. 点击 "Create new secret key"
5. 复制生成的 API Key（格式：`sk-...`）

**配置示例：**
```env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**注意事项：**
- API Key 以 `sk-` 开头
- 请妥善保管，不要泄露给他人
- 如果泄露，请立即在 OpenAI 平台删除并重新生成

## ⚙️ 可选配置

### 模型选择

```env
# 默认LLM模型（用于文本生成）
DEFAULT_LLM_MODEL=gpt-4

# 可选模型：
# - gpt-4: 最强大但较慢
# - gpt-3.5-turbo: 快速且经济
# - gpt-4-turbo: 平衡性能与速度

# 视觉语言模型（用于GUI智能体）
DEFAULT_VL_MODEL=gpt-4-vision-preview

# 可选模型：
# - gpt-4-vision-preview: 支持图像理解
# - gpt-4: 也支持图像（如果可用）
```

### 温度参数

```env
# 控制输出的随机性（0.0-2.0）
# 0.0: 更确定、一致
# 1.0: 平衡
# 2.0: 更随机、创造性
TEMPERATURE=0.1
```

### 任务执行配置

```env
# 最大执行步骤数
MAX_STEPS=10
```

## 🔄 不使用 API Key 的情况

**重要提示：** 即使没有配置 API Key，系统也可以运行，但功能会受限：

✅ **可以使用的功能：**
- 基本的任务解析（使用规则方法）
- 简单的GUI操作（基于规则）
- 系统架构和界面

❌ **无法使用的功能：**
- 智能任务分解（需要LLM）
- 复杂的屏幕理解（需要视觉模型）
- 智能代码生成
- 任务评估

## 📝 配置示例

### 完整配置示例

```env
# OpenAI API Key（必需）
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# 模型配置
DEFAULT_LLM_MODEL=gpt-4
DEFAULT_VL_MODEL=gpt-4-vision-preview
TEMPERATURE=0.1

# 执行配置
MAX_STEPS=10
```

### 最小配置示例（仅API Key）

```env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## 🔒 安全建议

1. **不要提交 `.env` 文件到 Git**
   - `.env` 文件已在 `.gitignore` 中
   - 确保不要意外提交

2. **使用环境变量（生产环境）**
   ```bash
   # Linux/Mac
   export OPENAI_API_KEY=sk-your-key-here
   
   # Windows PowerShell
   $env:OPENAI_API_KEY="sk-your-key-here"
   ```

3. **定期轮换 API Key**
   - 定期检查 API 使用情况
   - 如果发现异常，立即更换 Key

4. **设置使用限额**
   - 在 OpenAI 平台设置使用限额
   - 监控 API 调用成本

## 🧪 验证配置

### 方法1：运行测试

```bash
# 运行测试（会检查配置）
python run_tests.py
```

### 方法2：启动系统

```bash
# 启动系统
python run_demo.py

# 或直接启动Web界面
python main.py
```

如果配置正确，系统会显示智能体初始化成功的日志。

## ❓ 常见问题

### Q1: 没有 API Key 可以运行吗？

**A:** 可以，但功能受限。系统会使用规则方法作为备用方案。

### Q2: API Key 在哪里配置？

**A:** 在项目根目录的 `.env` 文件中配置。

### Q3: 如何检查配置是否正确？

**A:** 启动系统后，查看日志输出。如果看到"规划智能体初始化成功"等消息，说明配置正确。

### Q4: 可以使用其他 LLM 服务吗？

**A:** 当前版本主要支持 OpenAI。如需支持其他服务（如 DeepSeek、通义千问等），需要修改代码中的 LLM 初始化逻辑。

### Q5: API 调用费用如何？

**A:** 
- GPT-4: 约 $0.03/1K tokens（输入），$0.06/1K tokens（输出）
- GPT-3.5-turbo: 约 $0.0015/1K tokens（输入），$0.002/1K tokens（输出）
- GPT-4 Vision: 约 $0.01/图片

建议：
- 开发测试使用 GPT-3.5-turbo
- 生产环境根据需求选择

### Q6: 如何减少 API 调用成本？

**A:**
1. 使用 GPT-3.5-turbo 代替 GPT-4（适合简单任务）
2. 设置合理的 `MAX_STEPS` 限制
3. 优化任务描述，减少不必要的调用
4. 使用规则方法处理简单任务

## 📚 相关文档

- [OpenAI API 文档](https://platform.openai.com/docs)
- [OpenAI 定价](https://openai.com/pricing)
- [系统架构设计](docs/01-系统架构设计.md)
- [技术选型](docs/02-技术选型.md)

## 🆘 获取帮助

如果遇到配置问题，请：
1. 检查 `.env` 文件格式是否正确
2. 确认 API Key 是否有效
3. 查看系统日志中的错误信息
4. 参考 [README.md](README.md) 中的故障排除部分

