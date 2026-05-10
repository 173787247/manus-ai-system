# V1 — 骨架阶段（Skeleton）

本阶段对应「最小可运行的 Agent 抽象」：**统一生命周期与统计字段**，不含 GUI、不含完整编排。

## 目录说明

| 文件 | 作用 |
|------|------|
| `run_skeleton.py` | 独立可运行示例：`BaseAgent` + `EchoAgent`，无需仓库其余模块 |

## 运行

```bash
cd v1-skeleton
python run_skeleton.py
```

## 与主工程的关系

完整实现演进为仓库根目录的 `src/agents/base_agent.py` 及后续智能体模块；此处保留**最小教学快照**，便于对照渐进开发。
