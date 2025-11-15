#!/bin/bash
# 测试运行脚本 (Linux/Mac)

set -e

echo "=========================================="
echo "Manus AI 代理系统 - 测试套件"
echo "=========================================="
echo

# 检查是否在虚拟环境中
if [ -z "$VIRTUAL_ENV" ]; then
    echo "警告: 未检测到虚拟环境"
    echo "建议: source venv/bin/activate"
    echo
fi

# 运行测试
echo "1. 运行单元测试..."
pytest tests/test_base_agent.py -v
pytest tests/test_agent_manager.py -v
pytest tests/test_planning_agent.py -v
pytest tests/test_knowledge_agent.py -v
pytest tests/test_gui_agent.py -v

echo
echo "2. 运行核心模块测试..."
pytest tests/test_task_executor.py -v

echo
echo "3. 运行集成测试..."
pytest tests/test_integration.py -v -m integration

echo
echo "4. 生成覆盖率报告..."
pytest tests/ --cov=src --cov-report=html --cov-report=term

echo
echo "=========================================="
echo "测试完成！"
echo "覆盖率报告: htmlcov/index.html"
echo "=========================================="

