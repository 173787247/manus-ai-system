"""
Manus AI 代理系统 - 演示模式
无需API密钥即可体验系统功能
"""
import sys
import os
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

def main():
    """主函数 - 演示模式"""
    print("=" * 60)
    print("🤖 Manus AI 代理系统 - 演示模式")
    print("=" * 60)
    print()
    print("选择运行模式:")
    print("  1. Web界面 (推荐)")
    print("  2. 命令行界面")
    print("  3. 退出")
    print()
    
    choice = input("请选择 (1/2/3): ").strip()
    
    if choice == "1":
        print("\n启动Web界面...")
        print("浏览器将自动打开或访问: http://localhost:7860")
        print("按 Ctrl+C 停止服务")
        print("=" * 60)
        print()
        from src.ui.web_ui import main
        main()
    
    elif choice == "2":
        print("\n启动命令行界面...")
        print("=" * 60)
        print()
        from src.ui.cli import main
        main()
    
    elif choice == "3":
        print("退出")
        sys.exit(0)
    
    else:
        print("无效选择，退出")
        sys.exit(1)


if __name__ == "__main__":
    main()

