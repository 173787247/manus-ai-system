"""测试任务执行器"""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.task_executor import TaskExecutor


def test_task_executor_initialization():
    """测试任务执行器初始化"""
    config = {
        "agents": {},
        "max_steps": 10
    }
    
    executor = TaskExecutor(config)
    
    assert executor.config == config


def test_task_executor_execute_structure():
    """测试任务执行返回结构"""
    config = {
        "agents": {
            "planning": {
                "openai_api_key": None,
                "model": "gpt-4"
            }
        },
        "max_steps": 10
    }
    
    executor = TaskExecutor(config)
    
    task = {
        "instruction": "测试任务",
        "max_steps": 5
    }
    
    result = executor.execute(task)
    
    # 验证返回结构
    assert "status" in result
    assert "execution_time" in result
    
    # 如果有计划，验证结构
    if "plan" in result:
        assert "subtasks" in result["plan"] or result["plan"].get("status") == "error"

