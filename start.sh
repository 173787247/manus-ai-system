#!/bin/bash
# Manus AI 代理系统 - 启动脚本 (Linux/Mac)

echo "=========================================="
echo "Manus AI 代理系统"
echo "=========================================="
echo

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未找到Python，请先安装Python 3.9+"
    exit 1
fi

# 检查依赖
echo "[1/3] 检查依赖..."
if ! python3 -c "import gradio" 2>/dev/null; then
    echo "[警告] Gradio未安装，正在安装..."
    pip install gradio
fi

# 启动系统
echo "[2/3] 启动Web界面..."
echo
echo "=========================================="
echo "系统正在启动..."
echo "=========================================="
echo
echo "启动后，浏览器将自动打开或访问:"
echo "http://localhost:7860"
echo
echo "按 Ctrl+C 停止服务"
echo "=========================================="
echo

python3 main.py

