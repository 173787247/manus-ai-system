"""
Manus AI 代理系统 - 主入口文件
"""
import os
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from src.ui.web_ui import main

if __name__ == "__main__":
    main()

