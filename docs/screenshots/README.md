# 运行截图占位说明（毕业设计 / 课程提交）

请在本目录保存 **至少 3 张** 截图（PNG/JPG 均可），建议命名：

1. `01-ci-success.png` — GitHub Actions 流水线通过（或本地等价终端 pytest 全绿）。
2. `02-telegram-push.png` — Telegram 收到机器人消息（使用 `v4-production/scripts/telegram_notify.py`）。
3. `03-logs-or-cost.png` — 日志或成本统计（也可用仓库内 `03-cost-summary.txt` 佐证）。
4. **CI**：推送后在 GitHub **Actions** 截取绿色运行记录（即 `01-ci-success.png`）。

说明：若暂未导出 PNG，可使用已提交的 **`02-telegram-send-response.txt`**（`sendMessage` API 返回，`"ok":true`）与 **`03-cost-summary.txt`** 作为辅助材料；正式提交仍以 PNG 截图（手机 Telegram + 终端）为佳。

提交前将文件放入此目录并在根目录 `README.md` 中已有总体说明。
