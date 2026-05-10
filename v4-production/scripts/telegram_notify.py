"""
发送一条 Telegram 文本消息（用于「管线成功 / 任务完成」推送截图）。

需要环境变量:
  TELEGRAM_BOT_TOKEN  - BotFather 颁发的 token
  TELEGRAM_CHAT_ID    - 接收方 chat id

可选:
  TELEGRAM_MESSAGE    - 消息正文，默认 Manus pipeline notification
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request


def main() -> int:
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    text = os.environ.get(
        "TELEGRAM_MESSAGE", "Manus AI: pipeline / local check completed."
    ).strip()

    if not token or not chat_id:
        print(
            "Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID. See root .env.example.",
            file=sys.stderr,
        )
        return 1

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = json.dumps(
        {"chat_id": chat_id, "text": text},
        ensure_ascii=False,
    ).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8", errors="replace")
        print(body)
        data = json.loads(body)
        return 0 if data.get("ok") else 2
    except urllib.error.HTTPError as e:
        print(e.read().decode("utf-8", errors="replace"), file=sys.stderr)
        return 3
    except OSError as e:
        print(str(e), file=sys.stderr)
        return 4


if __name__ == "__main__":
    raise SystemExit(main())
