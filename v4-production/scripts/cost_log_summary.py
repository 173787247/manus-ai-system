"""
从 JSON Lines 成本日志打印汇总，便于「成本 / 调用统计」截图。

每行一条 JSON，示例:
  {"ts":"2026-05-10T12:00:00","model":"gpt-4","prompt_tokens":120,"completion_tokens":40,"cost_usd":0.001}

环境变量:
  MANUS_COST_LOG - 日志文件路径（默认 logs/manus_cost.jsonl）

若默认路径不存在且未设置 MANUS_COST_LOG，会尝试读取仓库内示例
  docs/sample_manus_cost.jsonl（便于本地演示与截图）。
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    default_log = root / "logs" / "manus_cost.jsonl"
    sample_log = root / "docs" / "sample_manus_cost.jsonl"

    if os.environ.get("MANUS_COST_LOG"):
        log_path = Path(os.environ["MANUS_COST_LOG"].strip())
        source = "MANUS_COST_LOG"
    elif default_log.is_file():
        log_path = default_log
        source = "default logs/manus_cost.jsonl"
    elif sample_log.is_file():
        log_path = sample_log
        source = "fallback docs/sample_manus_cost.jsonl"
    else:
        log_path = default_log
        source = "default (missing)"

    print("MANUS cost summary")
    print(f"log_path={log_path}")
    print(f"source={source}")

    if not log_path.is_file():
        print(
            "(no log file — create logs/manus_cost.jsonl or set MANUS_COST_LOG, "
            "or keep docs/sample_manus_cost.jsonl for demo)"
        )
        return 0

    lines = log_path.read_text(encoding="utf-8", errors="replace").strip().splitlines()
    if not lines:
        print("(empty log)")
        return 0

    total_cost = 0.0
    total_prompt = 0
    total_completion = 0
    n = 0
    for line in lines[-500:]:
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        n += 1
        total_prompt += int(row.get("prompt_tokens") or 0)
        total_completion += int(row.get("completion_tokens") or 0)
        total_cost += float(row.get("cost_usd") or 0.0)

    print(f"records_processed={n}")
    print(f"prompt_tokens_total={total_prompt}")
    print(f"completion_tokens_total={total_completion}")
    print(f"cost_usd_total={total_cost:.6f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
