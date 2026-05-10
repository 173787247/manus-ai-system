"""
轮询 Telegram getUpdates，直到你与机器人私聊发过消息（先点 Start 再发任意文字）。
用法（在仓库根目录）:
  python scripts/telegram_poll_chat_id.py

依赖：根目录 .env 中已配置 TELEGRAM_BOT_TOKEN（勿提交 Git）。
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.request
from pathlib import Path


def load_dotenv_file() -> None:
    root = Path(__file__).resolve().parents[1]
    p = root / ".env"
    if not p.is_file():
        return
    try:
        from dotenv import load_dotenv

        load_dotenv(p, override=False)
    except ImportError:
        for line in p.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            k, v = k.strip(), v.strip().strip('"').strip("'")
            if k and os.environ.get(k) is None:
                os.environ[k] = v


def main() -> int:
    load_dotenv_file()
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        print("请在 .env 中设置 TELEGRAM_BOT_TOKEN", file=sys.stderr)
        return 1

    print("请在 90 秒内打开手机 Telegram：打开 @rchuangmanusbot → Start → 发送任意文字（如 hi）")
    url = f"https://api.telegram.org/bot{token}/getUpdates"

    for i in range(45):
        try:
            with urllib.request.urlopen(url, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8", errors="replace"))
        except OSError as e:
            print(f"请求失败: {e}", file=sys.stderr)
            time.sleep(2)
            continue

        for up in data.get("result", []):
            msg = up.get("message") or up.get("edited_message")
            if not msg:
                continue
            chat = msg.get("chat") or {}
            cid = chat.get("id")
            if cid is not None:
                root = Path(__file__).resolve().parents[1]
                env_path = root / ".env"
                text = env_path.read_text(encoding="utf-8", errors="ignore")

                if re.search(r"(?m)^TELEGRAM_CHAT_ID=", text):
                    text = re.sub(
                        r"(?m)^TELEGRAM_CHAT_ID=.*$",
                        f"TELEGRAM_CHAT_ID={cid}",
                        text,
                    )
                else:
                    text += f"\nTELEGRAM_CHAT_ID={cid}\n"
                env_path.write_text(text, encoding="utf-8")
                print(f"\n已写入 {env_path}: TELEGRAM_CHAT_ID={cid}\n")
                return 0

        print(f"等待消息… ({i + 1}/45)")
        time.sleep(2)

    print(
        "\n超时：仍未收到消息。请确认已对机器人点 Start 并发过文字，然后重新运行本脚本。",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
