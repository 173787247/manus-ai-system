#!/usr/bin/env bash
# 提交前一键校验：V1 / V3 / 成本示例 / pytest
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

export PIP_INDEX_URL="${PIP_INDEX_URL:-https://pypi.tuna.tsinghua.edu.cn/simple}"
export PIP_TRUSTED_HOST="${PIP_TRUSTED_HOST:-pypi.tuna.tsinghua.edu.cn}"

echo "== [1/4] V1 skeleton =="
python v1-skeleton/run_skeleton.py

echo "== [2/4] V3 multi-agent =="
python v3-multi-agent/demo_run.py

echo "== [3/4] Cost summary (sample JSONL) =="
export MANUS_COST_LOG="$ROOT/docs/sample_manus_cost.jsonl"
python v4-production/scripts/cost_log_summary.py

echo "== [4/4] Pytest (full suite) =="
python -m pytest tests/ -v --tb=short

echo "== All checks finished OK =="
