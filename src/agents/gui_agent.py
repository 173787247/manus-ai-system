"""GUI操作智能体"""
from typing import Dict, Any, Optional, List
import logging
import base64
from io import BytesIO
from PIL import Image

from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


class GUIAgent(BaseAgent):
    """GUI操作智能体，负责屏幕观察与界面操作"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化GUI操作智能体
        
        Args:
            config: 配置字典
        """
        super().__init__("GUIAgent", config)
        self.env = self._init_desktop_env()
        self.vl_model = self._init_vl_model()
        self.action_parser = ActionParser()
    
    def _init_desktop_env(self):
        """初始化桌面环境"""
        # 简化实现：使用PyAutoGUI直接操作
        try:
            import pyautogui
            pyautogui.FAILSAFE = True
            pyautogui.PAUSE = 0.5
            return {"type": "pyautogui", "pyautogui": pyautogui}
        except Exception as e:
            logger.warning(f"桌面环境初始化失败: {e}")
            return None
    
    def _init_vl_model(self):
        """初始化视觉语言模型"""
        # 简化实现：实际应该初始化真实的VL模型
        try:
            from langchain_openai import ChatOpenAI
            api_key = self.config.get("openai_api_key")
            if api_key:
                return ChatOpenAI(
                    model=self.config.get("vl_model", "gpt-4-vision-preview"),
                    temperature=0.1,
                    api_key=api_key
                )
        except Exception as e:
            logger.warning(f"VL模型初始化失败: {e}")
        return None
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理输入数据
        
        Args:
            input_data: 输入数据字典
            
        Returns:
            处理结果
        """
        action = input_data.get("action", {})
        return self.execute_action(action)
    
    def observe(self) -> Dict[str, Any]:
        """
        观察屏幕
        
        Returns:
            观察结果
        """
        try:
            if not self.env:
                return {"status": "error", "message": "桌面环境未初始化"}
            
            import pyautogui
            screenshot = pyautogui.screenshot()
            
            # 转换为bytes
            img_bytes = BytesIO()
            screenshot.save(img_bytes, format='PNG')
            screenshot_bytes = img_bytes.getvalue()
            
            return {
                "status": "success",
                "screenshot": screenshot_bytes,
                "size": screenshot.size
            }
        except Exception as e:
            logger.error(f"屏幕观察失败: {e}")
            return {"status": "error", "message": str(e)}
    
    def think(self, observation: Dict[str, Any], task: str) -> Dict[str, Any]:
        """
        思考下一步动作
        
        Args:
            observation: 观察结果
            task: 任务描述
            
        Returns:
            思考结果
        """
        if not self.vl_model:
            return {
                "status": "error",
                "message": "VL模型未初始化",
                "actions": []
            }
        
        try:
            screenshot_bytes = observation.get("screenshot")
            if not screenshot_bytes:
                return {"status": "error", "message": "无截图数据", "actions": []}
            
            # 编码截图
            screenshot_b64 = base64.b64encode(screenshot_bytes).decode('utf-8')
            
            # 调用VL模型（简化实现）
            prompt = f"""
分析屏幕截图，根据任务描述生成操作步骤。

任务: {task}

请生成PyAutoGUI操作代码，例如：
- pyautogui.moveTo(x, y)  # 移动鼠标
- pyautogui.click()  # 点击
- pyautogui.typewrite("text")  # 输入文本

如果任务完成，返回 DONE
如果任务失败，返回 FAIL
如果需要等待，返回 WAIT
"""
            # 实际应该使用支持图像的VL模型API
            # 这里使用简化实现
            response = "pyautogui.moveTo(960, 540)\npyautogui.click()"
            
            return {
                "status": "success",
                "response": response,
                "actions": self.action_parser.parse(response)
            }
            
        except Exception as e:
            logger.error(f"思考过程失败: {e}")
            return {"status": "error", "message": str(e), "actions": []}
    
    def act(self, actions: List[str]) -> Dict[str, Any]:
        """
        执行动作
        
        Args:
            actions: 动作列表
            
        Returns:
            执行结果
        """
        if not self.env:
            return {"status": "error", "message": "桌面环境未初始化"}
        
        try:
            import pyautogui
            results = []
            
            for action in actions:
                if action in ["DONE", "FAIL"]:
                    return {"status": action, "results": results}
                
                if action == "WAIT":
                    import time
                    time.sleep(1)
                    continue
                
                # 执行PyAutoGUI命令
                try:
                    # 安全执行
                    exec(f"pyautogui.{action}", {"pyautogui": pyautogui})
                    results.append({"action": action, "status": "success"})
                except Exception as e:
                    logger.warning(f"动作执行失败: {action}, 错误: {e}")
                    results.append({"action": action, "status": "error", "error": str(e)})
            
            # 获取新的观察
            new_observation = self.observe()
            
            return {
                "status": "success",
                "results": results,
                "new_observation": new_observation
            }
            
        except Exception as e:
            logger.error(f"动作执行失败: {e}")
            return {"status": "error", "message": str(e)}
    
    def execute_action(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行动作（统一接口）
        
        Args:
            action: 动作字典
            
        Returns:
            执行结果
        """
        action_type = action.get("type", "unknown")
        
        if action_type == "observe":
            return self.observe()
        elif action_type == "think":
            observation = action.get("observation", {})
            task = action.get("task", "")
            return self.think(observation, task)
        elif action_type == "act":
            actions = action.get("actions", [])
            return self.act(actions)
        else:
            return {"status": "error", "message": f"未知动作类型: {action_type}"}
    
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行完整任务
        
        Args:
            task: 任务字典
            
        Returns:
            执行结果
        """
        self.set_state("working")
        
        try:
            instruction = task.get("instruction", "")
            max_steps = task.get("max_steps", 10)
            
            # 初始观察
            obs = self.observe()
            
            for step in range(max_steps):
                # 思考
                think_result = self.think(obs, instruction)
                actions = think_result.get("actions", [])
                
                if not actions:
                    break
                
                # 行动
                act_result = self.act(actions)
                
                if act_result["status"] in ["DONE", "FAIL"]:
                    break
                
                # 更新观察
                obs = act_result.get("new_observation", obs)
            
            self.set_state("idle")
            return {
                "status": "completed",
                "steps": step + 1,
                "final_observation": obs
            }
            
        except Exception as e:
            logger.error(f"任务执行失败: {e}")
            self.set_state("error")
            return {"status": "error", "message": str(e)}


class ActionParser:
    """动作解析器"""
    
    def __init__(self):
        import re
        self.re = re
    
    def parse(self, model_output: str) -> List[str]:
        """
        从模型输出解析动作
        
        Args:
            model_output: 模型输出文本
            
        Returns:
            动作列表
        """
        actions = []
        
        # 1. 提取代码块
        code_blocks = self._extract_code_blocks(model_output)
        
        # 2. 提取PyAutoGUI命令
        for block in code_blocks:
            pyautogui_commands = self._extract_pyautogui_commands(block)
            actions.extend(pyautogui_commands)
        
        # 3. 提取控制符
        control_chars = self._extract_control_chars(model_output)
        actions.extend(control_chars)
        
        # 4. 验证与过滤
        actions = self._validate_actions(actions)
        
        return actions if actions else ["FAIL"]
    
    def _extract_code_blocks(self, text: str) -> List[str]:
        """提取代码块"""
        pattern = r'```(?:python)?\n(.*?)```'
        matches = self.re.findall(pattern, text, self.re.DOTALL)
        return matches if matches else [text]
    
    def _extract_pyautogui_commands(self, code: str) -> List[str]:
        """提取PyAutoGUI命令"""
        pattern = r'pyautogui\.\w+\([^)]*\)'
        matches = self.re.findall(pattern, code)
        # 移除 pyautogui. 前缀，只保留方法调用部分
        return [match.replace("pyautogui.", "") for match in matches]
    
    def _extract_control_chars(self, text: str) -> List[str]:
        """提取控制符"""
        control_pattern = r'\b(DONE|FAIL|WAIT)\b'
        matches = self.re.findall(control_pattern, text, self.re.IGNORECASE)
        return [match.upper() for match in matches]
    
    def _validate_actions(self, actions: List[str]) -> List[str]:
        """验证动作"""
        validated = []
        whitelist = [
            "moveTo", "click", "doubleClick", "rightClick",
            "typewrite", "press", "keyDown", "keyUp",
            "scroll", "drag", "dragTo"
        ]
        
        for action in actions:
            if action in ["DONE", "FAIL", "WAIT"]:
                validated.append(action)
                continue
            
            # 检查是否在白名单中
            action_name = action.split("(")[0]
            if action_name in whitelist:
                validated.append(action)
        
        return validated

