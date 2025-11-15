"""评估智能体"""
from typing import Dict, Any
import logging

from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


class EvaluationAgent(BaseAgent):
    """评估智能体，负责任务完成度评估与反馈"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化评估智能体
        
        Args:
            config: 配置字典
        """
        super().__init__("EvaluationAgent", config)
        self.llm = self._init_llm()
    
    def _init_llm(self):
        """初始化LLM"""
        try:
            from langchain_openai import ChatOpenAI
            api_key = self.config.get("openai_api_key")
            if api_key:
                return ChatOpenAI(
                    model=self.config.get("model", "gpt-4"),
                    temperature=0.1,
                    api_key=api_key
                )
        except Exception as e:
            logger.warning(f"LLM初始化失败: {e}")
        return None
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理输入数据
        
        Args:
            input_data: 输入数据字典
            
        Returns:
            处理结果
        """
        task = input_data.get("task", {})
        execution_result = input_data.get("execution_result", {})
        return self.evaluate(task, execution_result)
    
    def evaluate(self, task: Dict[str, Any], execution_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        评估任务执行结果
        
        Args:
            task: 任务字典
            execution_result: 执行结果字典
            
        Returns:
            评估结果
        """
        self.set_state("working")
        
        try:
            # 1. 完成度评估
            completion = self._evaluate_completion(task, execution_result)
            
            # 2. 质量评估
            quality = self._evaluate_quality(execution_result)
            
            # 3. 问题识别
            issues = self._identify_issues(execution_result)
            
            # 4. 建议生成
            suggestions = self._generate_suggestions(issues)
            
            overall_status = "success" if completion > 0.8 else "partial"
            
            self.set_state("idle")
            return {
                "status": "success",
                "completion_score": completion,
                "quality_score": quality,
                "issues": issues,
                "suggestions": suggestions,
                "overall_status": overall_status
            }
            
        except Exception as e:
            logger.error(f"评估失败: {e}")
            self.set_state("error")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def _evaluate_completion(self, task: Dict[str, Any], 
                           result: Dict[str, Any]) -> float:
        """
        评估完成度
        
        Args:
            task: 任务字典
            result: 执行结果
            
        Returns:
            完成度分数 (0-1)
        """
        evaluator = task.get("evaluator")
        if not evaluator:
            # 如果没有评估器，根据执行状态判断
            status = result.get("status", "unknown")
            if status == "completed":
                return 1.0
            elif status == "partial":
                return 0.5
            else:
                return 0.0
        
        evaluator_type = evaluator.get("type", "unknown")
        
        if evaluator_type == "screenshot_check":
            return self._check_screenshot(result, evaluator)
        elif evaluator_type == "file_check":
            return self._check_file(result, evaluator)
        elif evaluator_type == "vm_command_line":
            return self._check_command_output(result, evaluator)
        else:
            return 0.5  # 默认值
    
    def _evaluate_quality(self, result: Dict[str, Any]) -> float:
        """
        评估质量
        
        Args:
            result: 执行结果
            
        Returns:
            质量分数 (0-1)
        """
        # 简化实现
        steps = result.get("steps", 0)
        errors = result.get("errors", [])
        
        if steps == 0:
            return 0.0
        
        error_rate = len(errors) / steps
        quality = max(0.0, 1.0 - error_rate)
        
        return quality
    
    def _identify_issues(self, result: Dict[str, Any]) -> list:
        """
        识别问题
        
        Args:
            result: 执行结果
            
        Returns:
            问题列表
        """
        issues = []
        
        # 检查错误
        errors = result.get("errors", [])
        for error in errors:
            issues.append({
                "type": "error",
                "severity": "high",
                "message": str(error)
            })
        
        # 检查执行时间
        execution_time = result.get("execution_time", 0)
        if execution_time > 60:  # 超过60秒
            issues.append({
                "type": "performance",
                "severity": "medium",
                "message": f"执行时间过长: {execution_time}秒"
            })
        
        return issues
    
    def _generate_suggestions(self, issues: list) -> list:
        """
        生成建议
        
        Args:
            issues: 问题列表
            
        Returns:
            建议列表
        """
        suggestions = []
        
        for issue in issues:
            if issue["type"] == "error":
                suggestions.append({
                    "type": "error_handling",
                    "suggestion": "增加错误处理和重试机制"
                })
            elif issue["type"] == "performance":
                suggestions.append({
                    "type": "optimization",
                    "suggestion": "优化执行步骤，减少不必要的操作"
                })
        
        return suggestions
    
    def _check_screenshot(self, result: Dict[str, Any], 
                         evaluator: Dict[str, Any]) -> float:
        """检查截图"""
        # 简化实现
        expected = evaluator.get("expected", "")
        observation = result.get("final_observation", {})
        
        if observation.get("status") == "success":
            return 0.8  # 假设有截图就认为部分完成
        return 0.0
    
    def _check_file(self, result: Dict[str, Any], 
                   evaluator: Dict[str, Any]) -> float:
        """检查文件"""
        import os
        expected_file = evaluator.get("expected", "")
        
        if os.path.exists(expected_file):
            return 1.0
        return 0.0
    
    def _check_command_output(self, result: Dict[str, Any], 
                             evaluator: Dict[str, Any]) -> float:
        """检查命令输出"""
        # 简化实现
        return 0.5

