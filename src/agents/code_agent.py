"""代码生成智能体"""
from typing import Dict, Any, Optional
import logging
import re

from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


class CodeAgent(BaseAgent):
    """代码生成智能体，负责动态代码生成与执行"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化代码生成智能体
        
        Args:
            config: 配置字典
        """
        super().__init__("CodeAgent", config)
        self.llm = self._init_llm()
        self.sandbox = self._init_sandbox()
    
    def _init_llm(self):
        """初始化LLM"""
        try:
            from langchain_openai import ChatOpenAI
            api_key = self.config.get("openai_api_key")
            if api_key:
                return ChatOpenAI(
                    model=self.config.get("model", "gpt-4"),
                    temperature=self.config.get("temperature", 0.2),
                    api_key=api_key
                )
        except Exception as e:
            logger.warning(f"LLM初始化失败: {e}")
        return None
    
    def _init_sandbox(self):
        """初始化代码沙箱"""
        # 简化实现：使用受限的执行环境
        return {"enabled": True, "restricted": True}
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理输入数据
        
        Args:
            input_data: 输入数据字典
            
        Returns:
            处理结果
        """
        task = input_data.get("task", {})
        context = input_data.get("context", "")
        return self.generate_code(task, context)
    
    def generate_code(self, task: Dict[str, Any], context: str = "") -> Dict[str, Any]:
        """
        生成代码
        
        Args:
            task: 任务字典
            context: 上下文信息
            
        Returns:
            代码生成结果
        """
        self.set_state("working")
        
        try:
            description = task.get("description", "")
            
            # 使用LLM生成代码（如果可用）
            if self.llm:
                prompt = f"""
根据以下任务和上下文，生成Python代码：

任务: {description}
上下文: {context}

要求：
1. 代码要完整可执行
2. 包含必要的错误处理
3. 返回结果要明确
4. 只返回代码，不要其他说明

代码：
"""
                try:
                    response = self.llm.invoke(prompt)
                    code = self._extract_code(response.content)
                except Exception as e:
                    logger.warning(f"LLM代码生成失败: {e}")
                    code = self._generate_code_rule_based(description)
            else:
                code = self._generate_code_rule_based(description)
            
            # 验证代码
            validation_result = self._validate_code(code)
            
            if validation_result["valid"]:
                self.set_state("idle")
                return {
                    "status": "success",
                    "code": code,
                    "validation": validation_result
                }
            else:
                self.set_state("error")
                return {
                    "status": "error",
                    "code": code,
                    "validation": validation_result,
                    "message": "代码验证失败"
                }
                
        except Exception as e:
            logger.error(f"代码生成失败: {e}")
            self.set_state("error")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def execute_code(self, code: str) -> Dict[str, Any]:
        """
        执行代码
        
        Args:
            code: 代码字符串
            
        Returns:
            执行结果
        """
        if not self.sandbox.get("enabled"):
            return {"status": "error", "message": "沙箱未启用"}
        
        try:
            # 安全检查
            if not self._is_safe(code):
                return {"status": "error", "message": "代码包含不安全操作"}
            
            # 在受限环境中执行
            restricted_globals = {
                "__builtins__": __builtins__,
                "print": print,
                "len": len,
                "str": str,
                "int": int,
                "float": float,
                "list": list,
                "dict": dict,
            }
            restricted_locals = {}
            
            exec(code, restricted_globals, restricted_locals)
            
            return {
                "status": "success",
                "result": restricted_locals.get("result", None)
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def _extract_code(self, text: str) -> str:
        """从文本中提取代码"""
        # 提取代码块
        code_pattern = r'```(?:python)?\n(.*?)```'
        matches = re.findall(code_pattern, text, re.DOTALL)
        if matches:
            return matches[0].strip()
        
        # 如果没有代码块，返回整个文本
        return text.strip()
    
    def _generate_code_rule_based(self, description: str) -> str:
        """基于规则生成代码"""
        # 简化实现
        code = f"""
# {description}
result = None
# TODO: 实现具体逻辑
"""
        return code
    
    def _validate_code(self, code: str) -> Dict[str, Any]:
        """验证代码"""
        try:
            compile(code, "<string>", "exec")
            return {"valid": True, "errors": []}
        except SyntaxError as e:
            return {
                "valid": False,
                "errors": [{"type": "syntax_error", "message": str(e)}]
            }
    
    def _is_safe(self, code: str) -> bool:
        """检查代码是否安全"""
        # 黑名单
        blacklist = [
            "import os",
            "import sys",
            "import subprocess",
            "__import__",
            "eval(",
            "exec(",
            "open(",
            "file(",
        ]
        
        code_lower = code.lower()
        for item in blacklist:
            if item in code_lower:
                return False
        
        return True

