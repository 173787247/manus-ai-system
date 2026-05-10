# 提交前一键校验：V1 / V3 / 成本示例 / pytest（任一步失败则退出码非 0）
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

$env:PIP_INDEX_URL = "https://pypi.tuna.tsinghua.edu.cn/simple"
$env:PIP_TRUSTED_HOST = "pypi.tuna.tsinghua.edu.cn"

Write-Host "== [1/4] V1 skeleton ==" -ForegroundColor Cyan
python v1-skeleton/run_skeleton.py

Write-Host "== [2/4] V3 multi-agent ==" -ForegroundColor Cyan
python v3-multi-agent/demo_run.py

Write-Host "== [3/4] Cost summary (sample JSONL) ==" -ForegroundColor Cyan
$sample = Join-Path $Root "docs/sample_manus_cost.jsonl"
$env:MANUS_COST_LOG = $sample
python v4-production/scripts/cost_log_summary.py

Write-Host "== [4/4] Pytest (full suite) ==" -ForegroundColor Cyan
python -m pytest tests/ -v --tb=short

Write-Host "== All checks finished OK ==" -ForegroundColor Green
