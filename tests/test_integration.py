"""集成测试"""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.agent_manager import AgentManager
from src.core.task_executor import TaskExecutor


@pytest.mark.integration
def test_simple_task_flow():
    """测试简单任务流程"""
    config = {
        "agents": {
            "planning": {
                "openai_api_key": None,  # 不使用真实API
                "model": "gpt-4",
                "temperature": 0.1
            },
            "knowledge": {
                "vector_collection": "test"
            },
            "code": {
                "openai_api_key": None,
                "model": "gpt-4"
            },
            "gui": {
                "openai_api_key": None,
                "vl_model": "gpt-4-vision-preview"
            },
            "evaluation": {
                "openai_api_key": None,
                "model": "gpt-4"
            }
        },
        "max_steps": 5
    }
    
    # 初始化执行器
    executor = TaskExecutor(config)
    
    # 简单任务
    task = {
        "instruction": "测试任务：打开记事本",
        "max_steps": 3
    }
    
    result = executor.execute(task)
    
    # 验证基本结构
    assert "status" in result
    assert result["status"] in ["completed", "error"]
    assert "execution_time" in result
    assert isinstance(result["execution_time"], (int, float))


@pytest.mark.integration
def test_agent_coordination():
    """测试智能体协调"""
    config = {
        "agents": {
            "planning": {
                "openai_api_key": None,
                "model": "gpt-4"
            }
        }
    }
    
    manager = AgentManager(config)
    
    # 验证智能体已初始化
    assert manager.get_agent("planning") is not None
    
    # 验证状态
    status = manager.get_agent_status()
    assert "planning" in status

