"""规划智能体"""
from typing import Dict, Any, List
import logging
import json

from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


class PlanningAgent(BaseAgent):
    """规划智能体，负责任务分解与执行规划"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化规划智能体
        
        Args:
            config: 配置字典
        """
        super().__init__("PlanningAgent", config)
        self.llm = self._init_llm()
    
    def _init_llm(self):
        """初始化LLM"""
        # 这里使用简化的实现，实际应该根据配置初始化真实的LLM
        try:
            from langchain_openai import ChatOpenAI
            api_key = self.config.get("openai_api_key")
            if api_key:
                return ChatOpenAI(
                    model=self.config.get("model", "gpt-4"),
                    temperature=self.config.get("temperature", 0.1),
                    api_key=api_key
                )
        except Exception as e:
            logger.warning(f"LLM初始化失败: {e}，将使用模拟实现")
        
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
        return self.decompose_task(task)
    
    def decompose_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        分解任务为子任务
        
        Args:
            task: 任务字典
            
        Returns:
            分解后的计划
        """
        self.set_state("working")
        
        try:
            # 1. 理解任务
            task_understanding = self._understand_task(task)
            
            # 2. 分解为子任务
            subtasks = self._decompose(task_understanding)
            
            # 3. 分析依赖
            dependencies = self._analyze_dependencies(subtasks)
            
            # 4. 生成执行计划
            plan = self._generate_plan(subtasks, dependencies)
            
            self.set_state("idle")
            return plan
            
        except Exception as e:
            logger.error(f"任务分解失败: {e}")
            self.set_state("error")
            return {
                "status": "error",
                "message": str(e),
                "subtasks": []
            }
    
    def _understand_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        理解任务意图
        
        Args:
            task: 任务字典
            
        Returns:
            任务理解结果
        """
        instruction = task.get("instruction", "")
        
        # 使用LLM理解任务（如果可用）
        if self.llm:
            prompt = f"""
分析以下任务，提取关键信息：
任务: {instruction}

请以JSON格式返回：
{{
    "goal": "任务目标",
    "steps": ["步骤1", "步骤2", ...],
    "resources": ["资源1", "资源2", ...],
    "expected_result": "预期结果",
    "keywords": ["关键词1", "关键词2", ...]
}}
"""
            try:
                response = self.llm.invoke(prompt)
                # 解析响应（简化实现）
                return self._parse_llm_response(response.content)
            except Exception as e:
                logger.warning(f"LLM理解失败: {e}，使用规则方法")
        
        # 规则方法（备用）
        return {
            "goal": instruction,
            "steps": self._extract_steps_rule_based(instruction),
            "resources": [],
            "expected_result": "任务完成",
            "keywords": self._extract_keywords(instruction)
        }
    
    def _decompose(self, task_understanding: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        分解任务为子任务
        
        Args:
            task_understanding: 任务理解结果
            
        Returns:
            子任务列表
        """
        steps = task_understanding.get("steps", [])
        subtasks = []
        
        for i, step in enumerate(steps):
            subtask = {
                "id": f"task_{i+1}",
                "description": step,
                "type": self._determine_task_type(step),
                "dependencies": []
            }
            subtasks.append(subtask)
        
        return subtasks
    
    def _analyze_dependencies(self, subtasks: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """
        分析子任务间的依赖关系
        
        Args:
            subtasks: 子任务列表
            
        Returns:
            依赖关系字典
        """
        dependencies = {}
        
        # 简单规则：按顺序依赖
        for i, subtask in enumerate(subtasks):
            deps = []
            if i > 0:
                deps.append(subtasks[i-1]["id"])
            dependencies[subtask["id"]] = deps
        
        return dependencies
    
    def _generate_plan(self, subtasks: List[Dict[str, Any]], 
                      dependencies: Dict[str, List[str]]) -> Dict[str, Any]:
        """
        生成执行计划
        
        Args:
            subtasks: 子任务列表
            dependencies: 依赖关系
            
        Returns:
            执行计划
        """
        # 更新子任务的依赖
        for subtask in subtasks:
            subtask["dependencies"] = dependencies.get(subtask["id"], [])
        
        # 生成执行顺序（拓扑排序）
        execution_order = self._topological_sort(subtasks, dependencies)
        
        return {
            "status": "success",
            "subtasks": subtasks,
            "execution_order": execution_order,
            "estimated_time": len(subtasks) * 5  # 估算时间（秒）
        }
    
    def _topological_sort(self, subtasks: List[Dict[str, Any]], 
                         dependencies: Dict[str, List[str]]) -> List[str]:
        """
        拓扑排序，确定执行顺序
        
        Args:
            subtasks: 子任务列表
            dependencies: 依赖关系
            
        Returns:
            执行顺序
        """
        # 简化实现：按顺序执行
        return [task["id"] for task in subtasks]
    
    def _determine_task_type(self, description: str) -> str:
        """
        确定任务类型
        
        Args:
            description: 任务描述
            
        Returns:
            任务类型
        """
        description_lower = description.lower()
        
        if any(keyword in description_lower for keyword in ["搜索", "查找", "检索"]):
            return "knowledge_query"
        elif any(keyword in description_lower for keyword in ["代码", "生成", "编写"]):
            return "code_generation"
        elif any(keyword in description_lower for keyword in ["点击", "输入", "打开", "移动"]):
            return "gui_action"
        else:
            return "unknown"
    
    def _extract_steps_rule_based(self, instruction: str) -> List[str]:
        """基于规则提取步骤"""
        # 简单实现：按句号或逗号分割
        steps = []
        for part in instruction.split("，"):
            part = part.strip()
            if part:
                steps.append(part)
        return steps if steps else [instruction]
    
    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        # 简单实现
        keywords = []
        common_keywords = ["打开", "搜索", "保存", "生成", "点击", "输入"]
        for keyword in common_keywords:
            if keyword in text:
                keywords.append(keyword)
        return keywords
    
    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        """解析LLM响应"""
        try:
            # 尝试解析JSON
            return json.loads(response)
        except:
            # 如果失败，返回默认值
            return {
                "goal": response,
                "steps": [],
                "resources": [],
                "expected_result": "",
                "keywords": []
            }

