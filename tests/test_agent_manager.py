"""测试智能体管理器"""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.agent_manager import AgentManager, MessageBus


def test_message_bus():
    """测试消息总线"""
    bus = MessageBus()
    received_messages = []
    
    def callback(message):
        received_messages.append(message)
    
    bus.subscribe("test_topic", callback)
    bus.publish("test_topic", {"data": "test"})
    
    assert len(received_messages) == 1
    assert received_messages[0]["data"] == "test"


def test_agent_manager_initialization():
    """测试智能体管理器初始化"""
    config = {
        "agents": {
            "planning": {
                "openai_api_key": "test_key",
                "model": "gpt-4"
            }
        }
    }
    
    manager = AgentManager(config)
    
    assert "planning" in manager.agents
    assert manager.get_agent("planning") is not None


def test_agent_manager_get_agent():
    """测试获取智能体"""
    config = {"agents": {}}
    manager = AgentManager(config)
    
    # 测试获取不存在的智能体
    assert manager.get_agent("nonexistent") is None


def test_agent_manager_register_agent():
    """测试注册智能体"""
    from src.agents.base_agent import BaseAgent
    
    class TestAgent(BaseAgent):
        def process(self, input_data):
            return {"status": "success"}
    
    config = {"agents": {}}
    manager = AgentManager(config)
    
    test_agent = TestAgent("TestAgent", {})
    manager.register_agent("test", test_agent)
    
    assert manager.get_agent("test") == test_agent


def test_agent_manager_status():
    """测试获取智能体状态"""
    config = {"agents": {}}
    manager = AgentManager(config)
    
    status = manager.get_agent_status()
    assert isinstance(status, dict)

