#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试运行脚本（修复编码问题版本）
"""
import sys
import subprocess
import os
from pathlib import Path

def run_tests():
    """运行所有测试"""
    project_root = Path(__file__).parent
    
    # 设置环境变量强制使用UTF-8
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'
    
    # 测试命令（简化版，避免配置文件问题）
    commands = [
        # 基础测试 - 不使用配置文件
        ["python", "-m", "pytest", "tests/test_base_agent.py", "-v", "--no-cov"],
        ["python", "-m", "pytest", "tests/test_agent_manager.py", "-v", "--no-cov"],
        
        # 智能体测试
        ["python", "-m", "pytest", "tests/test_planning_agent.py", "-v", "--no-cov"],
        ["python", "-m", "pytest", "tests/test_knowledge_agent.py", "-v", "--no-cov"],
        ["python", "-m", "pytest", "tests/test_gui_agent.py", "-v", "--no-cov"],
        
        # 核心模块测试
        ["python", "-m", "pytest", "tests/test_task_executor.py", "-v", "--no-cov"],
        
        # 集成测试
        ["python", "-m", "pytest", "tests/test_integration.py", "-v", "--no-cov", "-m", "integration"],
    ]
    
    print("=" * 60)
    print("Manus AI System - Test Suite (Fixed Version)")
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
                env=env,
                check=False,
                capture_output=False,
                encoding='utf-8',
                errors='replace'
            )
            results.append((cmd, result.returncode == 0))
        except Exception as e:
            print(f"Error: {e}")
            results.append((cmd, False))
    
    # 总结
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for cmd, success in results:
        status = "[PASS]" if success else "[FAIL]"
        test_file = cmd[3] if len(cmd) > 3 else "unknown"
        print(f"{status}: {test_file}")
    
    print(f"\nTotal: {passed}/{total} passed")
    
    if passed == total:
        print("\n[SUCCESS] All tests passed!")
        return 0
    else:
        print(f"\n[FAILED] {total - passed} tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(run_tests())

