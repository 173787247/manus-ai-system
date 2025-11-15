"""任务执行器"""
from typing import Dict, Any
import logging
import time

from .agent_manager import AgentManager

logger = logging.getLogger(__name__)


class TaskExecutor:
    """任务执行器，负责任务的统一执行"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化任务执行器
        
        Args:
            config: 配置字典
        """
        self.config = config
        self.agent_manager = None  # 延迟初始化
    
    def _init_agent_manager(self):
        """初始化智能体管理器"""
        if self.agent_manager is None:
            self.agent_manager = AgentManager(self.config.get("agents", {}))
    
    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行任务
        
        Args:
            task: 任务字典
            
        Returns:
            执行结果
        """
        self._init_agent_manager()
        
        start_time = time.time()
        
        try:
            # 1. 规划智能体分解任务
            planning_agent = self.agent_manager.get_agent("planning")
            if not planning_agent:
                execution_time = time.time() - start_time
                return {
                    "status": "error",
                    "message": "规划智能体未初始化",
                    "execution_time": execution_time
                }
            
            plan = planning_agent.decompose_task(task)
            
            if plan.get("status") == "error":
                execution_time = time.time() - start_time
                plan["execution_time"] = execution_time
                return plan
            
            # 2. 执行子任务
            results = []
            subtasks = plan.get("subtasks", [])
            execution_order = plan.get("execution_order", [])
            
            for task_id in execution_order:
                subtask = next((t for t in subtasks if t["id"] == task_id), None)
                if not subtask:
                    continue
                
                result = self._execute_subtask(subtask)
                results.append(result)
                
                # 如果子任务失败，停止执行
                if result.get("status") == "error":
                    break
            
            # 3. 评估结果
            evaluation_agent = self.agent_manager.get_agent("evaluation")
            evaluation = None
            if evaluation_agent:
                evaluation = evaluation_agent.evaluate(
                    task,
                    {"results": results, "steps": len(results)}
                )
            
            execution_time = time.time() - start_time
            
            return {
                "status": "completed",
                "plan": plan,
                "results": results,
                "evaluation": evaluation,
                "steps": len(results),
                "execution_time": execution_time
            }
            
        except Exception as e:
            logger.error(f"任务执行失败: {e}")
            return {
                "status": "error",
                "message": str(e),
                "execution_time": time.time() - start_time
            }
    
    def _execute_subtask(self, subtask: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行子任务
        
        Args:
            subtask: 子任务字典
            
        Returns:
            执行结果
        """
        subtask_type = subtask.get("type", "unknown")
        description = subtask.get("description", "")
        
        logger.info(f"执行子任务: {description} (类型: {subtask_type})")
        
        if subtask_type == "knowledge_query":
            knowledge_agent = self.agent_manager.get_agent("knowledge")
            if knowledge_agent:
                return knowledge_agent.retrieve(description)
        
        elif subtask_type == "code_generation":
            code_agent = self.agent_manager.get_agent("code")
            if code_agent:
                return code_agent.generate_code(subtask)
        
        elif subtask_type == "gui_action":
            gui_agent = self.agent_manager.get_agent("gui")
            if gui_agent:
                # 执行GUI任务
                gui_task = {
                    "instruction": description,
                    "max_steps": self.config.get("max_steps", 10)
                }
                return gui_agent.execute_task(gui_task)
        
        return {
            "status": "error",
            "message": f"未知的子任务类型: {subtask_type}"
        }

