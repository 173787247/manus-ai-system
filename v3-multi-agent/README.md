# V3 — 多智能体阶段（Multi-Agent）

本阶段对应：**AgentManager + 消息总线式协作**、规划 / 知识 / 代码 / GUI 等智能体由配置装配，与 `src/core/agent_manager.py` 一致。

## 运行（在仓库根目录）

需已安装依赖（见根目录 `requirements.txt` 或 `requirements-ci.txt`）。

```bash
python v3-multi-agent/demo_run.py
```

## 行为说明

- 使用**仅规划智能体**的轻量配置（无需有效 API Key 亦可初始化；任务分解走规则/回退逻辑）。
- 打印 `MessageBus` 与 `AgentManager` 的注册情况，验证多智能体管理器可运行。

## 与主工程的关系

生产级能力（Web UI、Docker、监控、Telegram 等）在 **V4** 与仓库根目录脚本中统一说明。
