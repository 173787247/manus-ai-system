"""将单次 LLM 调用的 token / 成本追加写入 logs/manus_cost.jsonl。"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def append_cost_record(
    *,
    model: str,
    prompt_tokens: int,
    completion_tokens: int,
    cost_usd: float | None = None,
    log_path: Path | None = None,
) -> Path:
    """
    追加一行 JSON（JSON Lines）。可与 OpenAI 返回的 usage 字段对应。
    """
    root = project_root()
    path = log_path or (root / "logs" / "manus_cost.jsonl")
    path.parent.mkdir(parents=True, exist_ok=True)
    row = {
        "ts": datetime.now().isoformat(timespec="seconds"),
        "model": model,
        "prompt_tokens": int(prompt_tokens),
        "completion_tokens": int(completion_tokens),
        "cost_usd": float(cost_usd if cost_usd is not None else 0.0),
    }
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    return path
