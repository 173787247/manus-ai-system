#!/usr/bin/env python
"""
测试运行脚本
"""
import sys
import subprocess
from pathlib import Path

def run_tests():
    """运行所有测试"""
    project_root = Path(__file__).parent
    
    # 测试命令
    commands = [
        # 基础测试
        ["pytest", "tests/test_base_agent.py", "-v"],
        ["pytest", "tests/test_agent_manager.py", "-v"],
        
        # 智能体测试
        ["pytest", "tests/test_planning_agent.py", "-v"],
        ["pytest", "tests/test_knowledge_agent.py", "-v"],
        ["pytest", "tests/test_gui_agent.py", "-v"],
        
        # 核心模块测试
        ["pytest", "tests/test_task_executor.py", "-v"],
        
        # 集成测试
        ["pytest", "tests/test_integration.py", "-v", "-m", "integration"],
        
        # 完整测试套件
        ["pytest", "tests/", "-v", "--cov=src", "--cov-report=term-missing"]
    ]
    
    print("=" * 60)
    print("Manus AI 代理系统 - 测试套件")
    print("=" * 60)
    print()
    
    results = []
    
    for i, cmd in enumerate(commands, 1):
        print(f"\n[{i}/{len(commands)}] 运行: {' '.join(cmd)}")
        print("-" * 60)
        
        try:
            result = subprocess.run(
                cmd,
                cwd=project_root,
                check=False,
                capture_output=False
            )
            results.append((cmd, result.returncode == 0))
        except Exception as e:
            print(f"错误: {e}")
            results.append((cmd, False))
    
    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for cmd, success in results:
        status = "✓ 通过" if success else "✗ 失败"
        print(f"{status}: {' '.join(cmd[:2])}")
    
    print(f"\n总计: {passed}/{total} 通过")
    
    if passed == total:
        print("\n✓ 所有测试通过！")
        return 0
    else:
        print(f"\n✗ {total - passed} 个测试失败")
        return 1


if __name__ == "__main__":
    sys.exit(run_tests())

