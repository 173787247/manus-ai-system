"""测试基础智能体"""
import pytest
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agents.base_agent import BaseAgent


class TestAgent(BaseAgent):
    """测试用的智能体"""
    
    def process(self, input_data):
        return {"status": "success", "data": input_data}


def test_base_agent_initialization():
    """测试基础智能体初始化"""
    agent = TestAgent("TestAgent", {"max_memory": 10})
    
    assert agent.name == "TestAgent"
    assert agent.state == "idle"
    assert len(agent.memory) == 0
    assert agent.statistics["tasks_completed"] == 0


def test_base_agent_process():
    """测试基础智能体处理"""
    agent = TestAgent("TestAgent", {})
    
    result = agent.process({"test": "data"})
    assert result["status"] == "success"
    assert result["data"]["test"] == "data"


def test_base_agent_reset():
    """测试基础智能体重置"""
    agent = TestAgent("TestAgent", {})
    agent.set_state("working")
    agent.add_to_memory({"test": "data"})
    
    agent.reset()
    
    assert agent.state == "idle"
    assert len(agent.memory) == 0


def test_base_agent_status():
    """测试获取智能体状态"""
    agent = TestAgent("TestAgent", {})
    status = agent.get_status()
    
    assert status["name"] == "TestAgent"
    assert status["state"] == "idle"
    assert "statistics" in status


def test_base_agent_statistics():
    """测试统计信息更新"""
    agent = TestAgent("TestAgent", {})
    
    agent.update_statistics(success=True, execution_time=1.0)
    agent.update_statistics(success=False, execution_time=2.0)
    
    assert agent.statistics["tasks_completed"] == 1
    assert agent.statistics["tasks_failed"] == 1
    assert agent.statistics["average_time"] == 1.5

