# 快速开始指南

## 1. 环境准备

### 1.1 系统要求

- Python 3.9+
- Docker Desktop (已安装)
- 256GB 内存
- RTX-5080 GPU (可选，用于加速)

### 1.2 安装依赖

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

## 2. 配置环境

### 2.1 复制环境变量文件

```bash
cp .env.example .env
```

### 2.2 编辑环境变量

编辑 `.env` 文件，配置必要的API密钥：

```bash
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
```

## 3. 启动系统

### 3.1 使用Docker Compose (推荐)

```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 3.2 直接运行

```bash
# 启动Web界面
python main.py

# 或
python src/ui/web_ui.py
```

访问 http://localhost:7860 使用Web界面。

## 4. 使用示例

### 4.1 基本任务

在Web界面输入任务指令，例如：

```
打开记事本，输入"Hello World"，保存为test.txt
```

### 4.2 复杂任务

```
打开浏览器，访问百度，搜索"AI Agent"，截图保存
```

### 4.3 使用API

```python
from src.core.agent_manager import AgentManager
from src.core.task_executor import TaskExecutor

# 初始化
config = {...}  # 加载配置
executor = TaskExecutor(config)

# 执行任务
task = {
    "instruction": "打开浏览器，搜索'AI Agent'",
    "max_steps": 10
}
result = executor.execute(task)
print(result)
```

## 5. 常见问题

### 5.1 依赖安装失败

如果某些依赖安装失败，可以尝试：

```bash
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

### 5.2 GPU支持

如果需要GPU支持，确保：

1. 安装了NVIDIA驱动
2. 安装了CUDA
3. 安装了对应的PyTorch版本

### 5.3 权限问题

在Linux/Mac上，可能需要：

```bash
sudo chmod +x scripts/*.sh
```

## 6. 下一步

- 查看 [系统架构设计](docs/01-系统架构设计.md)
- 查看 [技术选型](docs/02-技术选型.md)
- 查看 [智能体设计](docs/03-智能体设计.md)
- 查看 [部署指南](docs/06-部署与应用场景.md)

