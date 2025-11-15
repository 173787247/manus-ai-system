"""基础智能体类"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """基础智能体类，所有智能体的基类"""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        """
        初始化智能体
        
        Args:
            name: 智能体名称
            config: 配置字典
        """
        self.name = name
        self.config = config
        self.state = "idle"  # idle, working, error
        self.memory: List[Dict[str, Any]] = []
        self.statistics = {
            "tasks_completed": 0,
            "tasks_failed": 0,
            "average_time": 0.0,
            "total_time": 0.0
        }
        self.created_at = datetime.now()
        
    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理输入数据，返回结果
        
        Args:
            input_data: 输入数据字典
            
        Returns:
            处理结果字典
        """
        raise NotImplementedError("子类必须实现process方法")
    
    def reset(self):
        """重置智能体状态"""
        self.state = "idle"
        self.memory = []
        logger.info(f"{self.name} 状态已重置")
    
    def get_status(self) -> Dict[str, Any]:
        """
        获取智能体状态
        
        Returns:
            状态字典
        """
        return {
            "name": self.name,
            "state": self.state,
            "memory_length": len(self.memory),
            "statistics": self.statistics,
            "created_at": self.created_at.isoformat()
        }
    
    def update_statistics(self, success: bool, execution_time: float):
        """
        更新统计信息
        
        Args:
            success: 是否成功
            execution_time: 执行时间（秒）
        """
        if success:
            self.statistics["tasks_completed"] += 1
        else:
            self.statistics["tasks_failed"] += 1
        
        self.statistics["total_time"] += execution_time
        total_tasks = self.statistics["tasks_completed"] + self.statistics["tasks_failed"]
        if total_tasks > 0:
            self.statistics["average_time"] = self.statistics["total_time"] / total_tasks
    
    def add_to_memory(self, item: Dict[str, Any]):
        """
        添加到记忆
        
        Args:
            item: 记忆项
        """
        item["timestamp"] = datetime.now().isoformat()
        self.memory.append(item)
        
        # 限制记忆长度
        max_memory = self.config.get("max_memory", 100)
        if len(self.memory) > max_memory:
            self.memory = self.memory[-max_memory:]
    
    def set_state(self, state: str):
        """
        设置状态
        
        Args:
            state: 新状态
        """
        old_state = self.state
        self.state = state
        logger.debug(f"{self.name} 状态从 {old_state} 变为 {state}")
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, state={self.state})"

