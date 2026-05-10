# V4 — 生产化阶段（Production）

本阶段对应：**测试门禁、CI 工作流、容器编排、可观测与外部通知**（日志摘要、成本统计、Telegram）。

## 包含能力

| 项 | 位置 |
|----|------|
| GitHub Actions CI | `.github/workflows/ci.yml` |
| 本地/容器部署 | 根目录 `docker-compose.yml`、`Dockerfile` |
| Telegram 通知（可选） | `v4-production/scripts/telegram_notify.py` |
| 成本/调用摘要（日志） | `v4-production/scripts/cost_log_summary.py` |
| 运行主程序 | 根目录 `main.py`、`run_demo.py` |

## 快速验证

```bash
# 1) 与 CI 一致的轻量依赖
pip install -r requirements-ci.txt
pytest tests/ -v --tb=short

# 2) 成本摘要（可指向 JSONL 日志）
set MANUS_COST_LOG=logs\manus_cost.jsonl
python v4-production/scripts/cost_log_summary.py

# 3) Telegram（需环境变量，见根目录 .env.example）
python v4-production/scripts/telegram_notify.py
```

## 与 V1–V3 的关系

- V1：单一智能体抽象  
- V2：自动化测试与摘要  
- V3：多智能体管理器  
- **V4：在完整 `src/` 上叠加工程化与运维能力**（本目录以脚本与说明为主，主代码仍在仓库根 `src/`）
