"""
手动追加一行成本记录到 logs/manus_cost.jsonl（便于生成真实汇总截图）。

示例:
  python scripts/log_manus_cost.py --model gpt-4o-mini --prompt 120 --completion 80 --cost 0.00015

数字可从 OpenAI 控制台用量、或单次 API 响应里的 usage 字段抄写。
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.utils.cost_log import append_cost_record  # noqa: E402


def main() -> int:
    p = argparse.ArgumentParser(description="追加一行到 logs/manus_cost.jsonl")
    p.add_argument("--model", default="gpt-4o-mini", help="模型名")
    p.add_argument("--prompt", type=int, required=True, help="prompt_tokens")
    p.add_argument("--completion", type=int, required=True, help="completion_tokens")
    p.add_argument(
        "--cost",
        type=float,
        default=0.0,
        help="本次调用估算成本（美元），无则填 0",
    )
    args = p.parse_args()
    path = append_cost_record(
        model=args.model,
        prompt_tokens=args.prompt,
        completion_tokens=args.completion,
        cost_usd=args.cost,
    )
    print(f"appended -> {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
