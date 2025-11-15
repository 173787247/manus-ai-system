"""测试规划智能体"""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agents.planning_agent import PlanningAgent


def test_planning_agent_initialization():
    """测试规划智能体初始化"""
    config = {
        "openai_api_key": "test_key",
        "model": "gpt-4",
        "temperature": 0.1
    }
    
    agent = PlanningAgent(config)
    
    assert agent.name == "PlanningAgent"
    assert agent.state == "idle"


def test_planning_agent_decompose_task():
    """测试任务分解"""
    config = {
        "openai_api_key": None,  # 不使用真实API
        "model": "gpt-4"
    }
    
    agent = PlanningAgent(config)
    
    task = {
        "instruction": "打开浏览器，搜索AI Agent"
    }
    
    plan = agent.decompose_task(task)
    
    # 验证返回结构
    assert "status" in plan
    assert "subtasks" in plan or plan.get("status") == "error"
    
    # 如果有子任务，验证结构
    if "subtasks" in plan:
        for subtask in plan["subtasks"]:
            assert "id" in subtask
            assert "description" in subtask
            assert "type" in subtask


def test_planning_agent_determine_task_type():
    """测试任务类型判断"""
    config = {"openai_api_key": None}
    agent = PlanningAgent(config)
    
    assert agent._determine_task_type("搜索相关内容") == "knowledge_query"
    assert agent._determine_task_type("生成代码") == "code_generation"
    assert agent._determine_task_type("点击按钮") == "gui_action"


def test_planning_agent_extract_keywords():
    """测试关键词提取"""
    config = {"openai_api_key": None}
    agent = PlanningAgent(config)
    
    keywords = agent._extract_keywords("打开浏览器，搜索内容，保存文件")
    
    assert len(keywords) > 0
    assert "打开" in keywords or "搜索" in keywords or "保存" in keywords

