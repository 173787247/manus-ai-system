"""
根据当前 cost_log_summary 终端输出渲染一张 PNG（深色终端风格），用于作业截图。
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("需要 Pillow: pip install Pillow", file=sys.stderr)
    raise SystemExit(1)


def _font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in (
        r"C:\Windows\Fonts\consola.ttf",
        r"C:\Windows\Fonts\cour.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    ):
        if Path(path).is_file():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def main() -> int:
    env = os.environ.copy()
    env.pop("MANUS_COST_LOG", None)

    proc = subprocess.run(
        [sys.executable, str(ROOT / "v4-production/scripts/cost_log_summary.py")],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )
    block = (
        "PS> python v4-production/scripts/cost_log_summary.py\n"
        + proc.stdout
        + ("PS> " if not proc.stdout.endswith("\n") else "PS> ")
    )
    if proc.stderr:
        block += "\n" + proc.stderr

    lines = block.splitlines()
    font = _font(18)
    pad_x, pad_y = 24, 24
    line_h = font.getbbox("Ay")[3] - font.getbbox("Ay")[1] + 6
    max_w = max(font.getlength(line) for line in lines) if lines else 200
    w = int(max_w + pad_x * 2)
    h = int(len(lines) * line_h + pad_y * 2)

    img = Image.new("RGB", (w, h), (24, 24, 28))
    draw = ImageDraw.Draw(img)
    fg = (220, 220, 210)
    prompt_color = (140, 200, 140)

    y = pad_y
    for i, line in enumerate(lines):
        color = prompt_color if line.startswith("PS>") else fg
        draw.text((pad_x, y), line, fill=color, font=font)
        y += line_h

    out = ROOT / "docs" / "screenshots" / "03-logs-or-cost.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "PNG")
    print(f"saved -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
