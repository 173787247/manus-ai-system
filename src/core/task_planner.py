"""任务规划器"""
from typing import Dict, Any
import logging

from .agent_manager import AgentManager

logger = logging.getLogger(__name__)


class TaskPlanner:
    """任务规划器，负责任务规划"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化任务规划器
        
        Args:
            config: 配置字典
        """
        self.config = config
        self.agent_manager = None  # 延迟初始化
    
    def _init_agent_manager(self):
        """初始化智能体管理器"""
        if self.agent_manager is None:
            self.agent_manager = AgentManager(self.config.get("agents", {}))
    
    def plan(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        规划任务
        
        Args:
            task: 任务字典
            
        Returns:
            执行计划
        """
        self._init_agent_manager()
        
        planning_agent = self.agent_manager.get_agent("planning")
        if not planning_agent:
            return {"status": "error", "message": "规划智能体未初始化"}
        
        return planning_agent.decompose_task(task)
    
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行任务（便捷方法）
        
        Args:
            task: 任务字典
            
        Returns:
            执行结果
        """
        from .task_executor import TaskExecutor
        executor = TaskExecutor(self.config)
        return executor.execute(task)

