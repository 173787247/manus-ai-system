"""多智能体管理器"""
from typing import Dict, Any, List, Optional
import logging
from collections import defaultdict

from ..agents.base_agent import BaseAgent
from ..agents.planning_agent import PlanningAgent
from ..agents.knowledge_agent import KnowledgeAgent
from ..agents.code_agent import CodeAgent
from ..agents.gui_agent import GUIAgent
from ..agents.evaluation_agent import EvaluationAgent

logger = logging.getLogger(__name__)


class MessageBus:
    """消息总线，用于智能体间通信"""
    
    def __init__(self):
        self.subscribers: Dict[str, List[callable]] = defaultdict(list)
        self.message_history: List[Dict[str, Any]] = []
    
    def publish(self, topic: str, message: Dict[str, Any]):
        """
        发布消息
        
        Args:
            topic: 主题
            message: 消息内容
        """
        message["topic"] = topic
        message["timestamp"] = self._get_timestamp()
        self.message_history.append(message)
        
        # 通知订阅者
        for callback in self.subscribers.get(topic, []):
            try:
                callback(message)
            except Exception as e:
                logger.error(f"消息回调执行失败: {e}")
    
    def subscribe(self, topic: str, callback: callable):
        """
        订阅消息
        
        Args:
            topic: 主题
            callback: 回调函数
        """
        self.subscribers[topic].append(callback)
    
    def _get_timestamp(self) -> str:
        """获取时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()


class AgentManager:
    """多智能体管理器"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化智能体管理器
        
        Args:
            config: 配置字典
        """
        self.config = config
        self.agents: Dict[str, BaseAgent] = {}
        self.message_bus = MessageBus()
        self._initialize_agents()
    
    def _initialize_agents(self):
        """初始化所有智能体"""
        agent_configs = self.config.get("agents", {})
        
        # 初始化规划智能体
        if "planning" in agent_configs:
            self.agents["planning"] = PlanningAgent(agent_configs["planning"])
        
        # 初始化知识智能体
        if "knowledge" in agent_configs:
            self.agents["knowledge"] = KnowledgeAgent(agent_configs["knowledge"])
        
        # 初始化代码智能体
        if "code" in agent_configs:
            self.agents["code"] = CodeAgent(agent_configs["code"])
        
        # 初始化GUI智能体
        if "gui" in agent_configs:
            self.agents["gui"] = GUIAgent(agent_configs["gui"])
        
        # 初始化评估智能体
        if "evaluation" in agent_configs:
            self.agents["evaluation"] = EvaluationAgent(agent_configs["evaluation"])
        
        logger.info(f"已初始化 {len(self.agents)} 个智能体: {list(self.agents.keys())}")
    
    def get_agent(self, agent_name: str) -> Optional[BaseAgent]:
        """
        获取智能体
        
        Args:
            agent_name: 智能体名称
            
        Returns:
            智能体实例，如果不存在返回None
        """
        return self.agents.get(agent_name)
    
    def register_agent(self, name: str, agent: BaseAgent):
        """
        注册智能体
        
        Args:
            name: 智能体名称
            agent: 智能体实例
        """
        self.agents[name] = agent
        logger.info(f"已注册智能体: {name}")
    
    def get_all_agents(self) -> Dict[str, BaseAgent]:
        """
        获取所有智能体
        
        Returns:
            智能体字典
        """
        return self.agents.copy()
    
    def get_agent_status(self) -> Dict[str, Any]:
        """
        获取所有智能体状态
        
        Returns:
            状态字典
        """
        return {
            name: agent.get_status()
            for name, agent in self.agents.items()
        }
    
    def reset_all_agents(self):
        """重置所有智能体"""
        for agent in self.agents.values():
            agent.reset()
        logger.info("所有智能体已重置")
    
    def coordinate_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        协调任务执行
        
        Args:
            task: 任务字典
            
        Returns:
            执行结果
        """
        # 1. 规划智能体分解任务
        planning_agent = self.get_agent("planning")
        if not planning_agent:
            return {"status": "error", "message": "规划智能体未初始化"}
        
        plan = planning_agent.decompose_task(task)
        
        # 2. 根据计划协调各智能体执行
        results = []
        for subtask in plan.get("subtasks", []):
            result = self._execute_subtask(subtask)
            results.append(result)
        
        # 3. 评估智能体评估结果
        evaluation_agent = self.get_agent("evaluation")
        if evaluation_agent:
            evaluation = evaluation_agent.evaluate(task, {"results": results})
        else:
            evaluation = {"status": "skipped"}
        
        return {
            "status": "completed",
            "plan": plan,
            "results": results,
            "evaluation": evaluation
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
        
        if subtask_type == "knowledge_query":
            knowledge_agent = self.get_agent("knowledge")
            if knowledge_agent:
                return knowledge_agent.retrieve(subtask.get("query", ""))
        
        elif subtask_type == "code_generation":
            code_agent = self.get_agent("code")
            if code_agent:
                return code_agent.generate_code(subtask)
        
        elif subtask_type == "gui_action":
            gui_agent = self.get_agent("gui")
            if gui_agent:
                return gui_agent.execute_action(subtask)
        
        return {"status": "error", "message": f"未知的子任务类型: {subtask_type}"}
    
    @property
    def planning_agent(self) -> Optional[PlanningAgent]:
        """获取规划智能体"""
        return self.get_agent("planning")
    
    @property
    def knowledge_agent(self) -> Optional[KnowledgeAgent]:
        """获取知识智能体"""
        return self.get_agent("knowledge")
    
    @property
    def code_agent(self) -> Optional[CodeAgent]:
        """获取代码智能体"""
        return self.get_agent("code")
    
    @property
    def gui_agent(self) -> Optional[GUIAgent]:
        """获取GUI智能体"""
        return self.get_agent("gui")
    
    @property
    def evaluation_agent(self) -> Optional[EvaluationAgent]:
        """获取评估智能体"""
        return self.get_agent("evaluation")

