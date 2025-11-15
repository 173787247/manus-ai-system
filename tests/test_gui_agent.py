"""测试GUI智能体"""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agents.gui_agent import GUIAgent, ActionParser


def test_gui_agent_initialization():
    """测试GUI智能体初始化"""
    config = {
        "openai_api_key": "test_key",
        "vl_model": "gpt-4-vision-preview"
    }
    
    agent = GUIAgent(config)
    
    assert agent.name == "GUIAgent"
    assert agent.state == "idle"


def test_action_parser():
    """测试动作解析器"""
    parser = ActionParser()
    
    # 测试提取PyAutoGUI命令
    code = "pyautogui.moveTo(100, 200)\npyautogui.click()"
    commands = parser._extract_pyautogui_commands(code)
    
    assert len(commands) == 2
    assert "moveTo(100, 200)" in commands or "moveTo" in commands[0]
    
    # 测试提取控制符
    text = "任务完成 DONE"
    control_chars = parser._extract_control_chars(text)
    
    assert "DONE" in control_chars


def test_action_parser_validate():
    """测试动作验证"""
    parser = ActionParser()
    
    actions = [
        "moveTo(100, 200)",  # 有效
        "click()",  # 有效
        "dangerous_operation()",  # 无效
        "DONE"  # 控制符
    ]
    
    validated = parser._validate_actions(actions)
    
    # 应该保留有效动作和控制符
    assert "DONE" in validated
    assert len(validated) >= 2


def test_action_parser_parse():
    """测试完整解析流程"""
    parser = ActionParser()
    
    model_output = """
    我看到需要点击按钮。
    ```python
    pyautogui.moveTo(500, 300)
    pyautogui.click()
    ```
    任务完成 DONE
    """
    
    actions = parser.parse(model_output)
    
    assert len(actions) > 0
    assert "DONE" in actions or any("moveTo" in a or "click" in a for a in actions)

