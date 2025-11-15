@echo off
REM Manus AI 代理系统 - 启动脚本 (Windows)
chcp 65001 >nul
echo ==========================================
echo Manus AI 代理系统
echo ==========================================
echo.

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python，请先安装Python 3.9+
    pause
    exit /b 1
)

REM 检查依赖
echo [1/3] 检查依赖...
python -c "import gradio" >nul 2>&1
if errorlevel 1 (
    echo [警告] Gradio未安装，正在安装...
    pip install gradio
)

REM 启动系统
echo [2/3] 启动Web界面...
echo.
echo ==========================================
echo 系统正在启动...
echo ==========================================
echo.
echo 启动后，浏览器将自动打开或访问:
echo http://localhost:7860
echo.
echo 按 Ctrl+C 停止服务
echo ==========================================
echo.

python main.py

pause

