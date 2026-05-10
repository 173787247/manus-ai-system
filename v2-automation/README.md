# V2 — 自动化阶段（Automation）

本阶段对应：**可重复的本地流水线**——一键安装依赖、运行测试并生成简要摘要，为 CI/CD 与后续工程化打基础。

## 目录说明

| 文件 | 作用 |
|------|------|
| `run_checks.py` | 在项目根目录执行 `pip install`（可选）与 `pytest`，将摘要写入 `output/run_summary.txt` |

## 运行（在仓库根目录）

```bash
# 仅运行检查（使用当前环境）
python v2-automation/run_checks.py

# 安装依赖后再测（需联网）。国内可使用清华 PyPI 镜像加速 pip 拉包：
# Windows PowerShell:
$env:PIP_INDEX_URL="https://pypi.tuna.tsinghua.edu.cn/simple"
$env:PIP_TRUSTED_HOST="pypi.tuna.tsinghua.edu.cn"
python v2-automation/run_checks.py --install

# Linux / macOS:
# export PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
# export PIP_TRUSTED_HOST=pypi.tuna.tsinghua.edu.cn
# python v2-automation/run_checks.py --install
```

说明：未设置 `PIP_INDEX_URL` 时，`--install` 使用 pip 默认源（国外 PyPI）。

## 输出

- `v2-automation/output/run_summary.txt`：退出码、部分 pytest 输出尾部（可用于日志截图）

## 与主工程的关系

GitHub Actions 见仓库 `.github/workflows/ci.yml`；本地脚本用于与 CI **同源验证**。
