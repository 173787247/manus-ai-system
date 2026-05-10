"""
V2 自动化：在项目根目录运行 pytest，并写入简要摘要（便于日志截图）。
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = Path(__file__).resolve().parent / "output"
SUMMARY = OUT_DIR / "run_summary.txt"


def _pip_index_args() -> list[str]:
    """若设置 PIP_INDEX_URL（如清华镜像），则为 pip install 追加 -i 与 --trusted-host。"""
    index = os.environ.get("PIP_INDEX_URL", "").strip()
    if not index:
        return []
    trusted = os.environ.get("PIP_TRUSTED_HOST", "").strip()
    if not trusted:
        trusted = urlparse(index).hostname or ""
    extra = ["-i", index]
    if trusted:
        extra.extend(["--trusted-host", trusted])
    return extra


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--install",
        action="store_true",
        help="先在仓库根目录 pip install -r requirements-ci.txt",
    )
    args = parser.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    lines: list[str] = []
    lines.append(f"time={datetime.now().isoformat()}")
    lines.append(f"root={ROOT}")

    if args.install:
        cmd = [
            sys.executable,
            "-m",
            "pip",
            "install",
            *_pip_index_args(),
            "-r",
            str(ROOT / "requirements-ci.txt"),
        ]
        lines.append("cmd_install=" + " ".join(cmd))
        r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        lines.append(f"install_exit={r.returncode}")
        if r.stdout:
            lines.append("--- pip stdout tail ---")
            lines.extend(r.stdout.splitlines()[-30:])
        if r.stderr and r.returncode != 0:
            lines.append("--- pip stderr tail ---")
            lines.extend(r.stderr.splitlines()[-30:])

    pytest_cmd = [
        sys.executable,
        "-m",
        "pytest",
        str(ROOT / "tests"),
        "-v",
        "--tb=short",
    ]
    lines.append("cmd_pytest=" + " ".join(pytest_cmd))
    pr = subprocess.run(pytest_cmd, cwd=ROOT, capture_output=True, text=True)
    lines.append(f"pytest_exit={pr.returncode}")
    tail = (pr.stdout or "") + "\n" + (pr.stderr or "")
    tail_lines = tail.strip().splitlines()[-40:] if tail.strip() else ["(no output)"]
    lines.append("--- pytest tail ---")
    lines.extend(tail_lines)

    SUMMARY.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(SUMMARY.read_text(encoding="utf-8"))
    return pr.returncode


if __name__ == "__main__":
    sys.exit(main())
