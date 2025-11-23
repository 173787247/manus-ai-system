"""基于 RASCEF 框架的智能客服 Agent - 电信套餐推荐"""
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import logging
import json

from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


@dataclass
class TelecomPackage:
    """电信套餐数据模型"""
    name: str  # 套餐名称
    price: float  # 价格（元/月）
    data: str  # 流量（G/月）
    calls: int  # 通话（分钟/月）
    target_group: str  # 适用人群
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "套餐名称": self.name,
            "价格(元/月)": self.price,
            "流量(G/月)": self.data,
            "通话(分钟/月)": self.calls,
            "适用人群": self.target_group
        }


class CustomerServiceAgent(BaseAgent):
    """基于 RASCEF 框架的智能客服 Agent"""
    
    # 电信套餐数据库
    PACKAGES = [
        TelecomPackage("经济卡", 29, "20", 100, "无限制"),
        TelecomPackage("关爱卡", 9, "5", 10, "60岁以上"),
        TelecomPackage("校园卡", 39, "200", 100, "在校生"),
        TelecomPackage("无限卡", 199, "无限", 500, "无限制"),
        TelecomPackage("精英卡", 99, "200", 500, "无限制"),
    ]
    
    def __init__(self, name: str = "智能客服", config: Optional[Dict[str, Any]] = None):
        """初始化智能客服 Agent"""
        if config is None:
            config = {
                "model": "gpt-4",
                "temperature": 0.7,
                "max_memory": 50,
                "use_chain_of_thought": True
            }
        super().__init__(name, config)
        self.conversation_history: List[Dict[str, str]] = []
        
    def _build_rascef_prompt(self, user_message: str) -> str:
        """
        使用 RASCEF 框架构建 Prompt
        
        RASCEF 框架：
        - R (Role): 角色定义
        - A (Action): 行动/任务
        - S (Situation): 情境/场景
        - C (Context): 上下文信息
        - E (Example): 示例
        - F (Format): 输出格式
        """
        # R: 角色定义
        role = """你是一位专业的电信套餐推荐智能客服，具有以下特点：
- 专业：深入了解所有电信套餐的特点和适用场景
- 友好：用温暖、耐心的语气与用户交流
- 精准：根据用户需求推荐最合适的套餐
- 结构化：使用清晰的逻辑和格式输出推荐结果"""
        
        # A: 行动/任务
        action = """你的任务是：
1. 理解用户的需求和背景信息（年龄、身份、使用习惯、预算等）
2. 使用思维链（Chain of Thought）分析用户需求
3. 从可用的套餐中选择最合适的推荐
4. 以结构化的方式展示推荐结果和理由"""
        
        # S: 情境/场景
        situation = f"""当前对话情境：
- 用户消息：{user_message}
- 对话历史：{self._format_conversation_history()}
- 可用套餐：{self._format_packages()}"""
        
        # C: 上下文信息
        context = """上下文信息：
- 用户是新用户，需要推荐合适的电信套餐
- 需要考虑的因素：价格、流量需求、通话需求、适用人群限制
- 如果用户信息不足，需要友好地询问更多信息"""
        
        # E: 示例
        example = """示例对话：

用户：我是大学生，平时用流量比较多，预算有限
客服思考过程：
1. 用户身份：在校生 → 符合"校园卡"的适用人群
2. 需求分析：流量需求大，预算有限
3. 套餐对比：
   - 校园卡：39元/月，200G流量，100分钟通话，适合在校生
   - 经济卡：29元/月，20G流量，100分钟通话，流量可能不够
4. 推荐：校园卡最合适，虽然价格稍高，但流量充足且符合身份

推荐结果：
【推荐套餐】校园卡
【价格】39元/月
【流量】200G/月
【通话】100分钟/月
【推荐理由】
1. 符合您的在校生身份
2. 200G流量满足您的使用需求
3. 价格适中，性价比高"""
        
        # F: 输出格式
        format_spec = """输出格式要求：
1. 首先展示思考过程（如果启用思维链）
2. 然后以结构化格式输出推荐结果：
   【推荐套餐】套餐名称
   【价格】XX元/月
   【流量】XX G/月
   【通话】XX 分钟/月
   【推荐理由】
   1. 理由1
   2. 理由2
   3. 理由3
3. 如果信息不足，友好地询问缺失的信息"""
        
        # 组合完整的 RASCEF Prompt
        prompt = f"""{role}

{action}

{situation}

{context}

{example}

{format_spec}

请根据以上框架，为用户提供专业的套餐推荐服务。"""
        
        return prompt
    
    def _format_packages(self) -> str:
        """格式化套餐信息"""
        packages_str = "\n".join([
            f"- {pkg.name}: {pkg.price}元/月, {pkg.data}G流量, {pkg.calls}分钟通话, 适用：{pkg.target_group}"
            for pkg in self.PACKAGES
        ])
        return packages_str
    
    def _format_conversation_history(self, max_turns: int = 5) -> str:
        """格式化对话历史"""
        if not self.conversation_history:
            return "（无历史对话）"
        
        recent_history = self.conversation_history[-max_turns:]
        history_str = "\n".join([
            f"用户：{item.get('user', '')}\n客服：{item.get('assistant', '')}"
            for item in recent_history
        ])
        return history_str
    
    def _analyze_user_needs(self, user_message: str) -> Dict[str, Any]:
        """
        分析用户需求（思维链推理）
        这里使用简化的规则引擎，实际应用中可以使用 LLM
        """
        needs = {
            "age_group": None,  # 年龄段
            "identity": None,  # 身份（学生、老人等）
            "budget": None,  # 预算
            "data_need": None,  # 流量需求（高/中/低）
            "call_need": None,  # 通话需求（高/中/低）
        }
        
        message_lower = user_message.lower()
        
        # 识别身份
        if any(word in message_lower for word in ["学生", "在校", "大学", "校园"]):
            needs["identity"] = "在校生"
        elif any(word in message_lower for word in ["老人", "60", "退休", "年长"]):
            needs["identity"] = "60岁以上"
        
        # 识别预算
        if any(word in message_lower for word in ["便宜", "经济", "预算有限", "省钱"]):
            needs["budget"] = "低"
        elif any(word in message_lower for word in ["高端", "无限", "不差钱"]):
            needs["budget"] = "高"
        else:
            needs["budget"] = "中"
        
        # 识别流量需求
        if any(word in message_lower for word in ["流量多", "流量大", "看视频", "玩游戏"]):
            needs["data_need"] = "高"
        elif any(word in message_lower for word in ["流量少", "基本不用"]):
            needs["data_need"] = "低"
        else:
            needs["data_need"] = "中"
        
        # 识别通话需求
        if any(word in message_lower for word in ["电话多", "通话多", "经常打电话"]):
            needs["call_need"] = "高"
        elif any(word in message_lower for word in ["很少打电话", "基本不打电话"]):
            needs["call_need"] = "低"
        else:
            needs["call_need"] = "中"
        
        return needs
    
    def _recommend_package(self, needs: Dict[str, Any]) -> Tuple[TelecomPackage, List[str], List[str]]:
        """
        根据用户需求推荐套餐（使用思维链推理）
        返回：(推荐套餐, 推荐理由列表)
        """
        reasoning_steps = []
        candidates = []
        
        # 步骤1：根据身份筛选
        reasoning_steps.append("【步骤1】根据用户身份筛选套餐")
        if needs["identity"] == "在校生":
            candidates = [pkg for pkg in self.PACKAGES if "校园" in pkg.name]
            reasoning_steps.append(f"  用户是在校生，筛选出：{[p.name for p in candidates]}")
        elif needs["identity"] == "60岁以上":
            candidates = [pkg for pkg in self.PACKAGES if "关爱" in pkg.name]
            reasoning_steps.append(f"  用户是60岁以上，筛选出：{[p.name for p in candidates]}")
        else:
            candidates = [pkg for pkg in self.PACKAGES if pkg.target_group == "无限制"]
            reasoning_steps.append(f"  用户无特殊身份限制，筛选出：{[p.name for p in candidates]}")
        
        if not candidates:
            candidates = self.PACKAGES.copy()
            reasoning_steps.append("  未找到身份匹配的套餐，考虑所有套餐")
        
        # 步骤2：根据预算筛选
        reasoning_steps.append("\n【步骤2】根据预算筛选套餐")
        if needs["budget"] == "低":
            candidates = [pkg for pkg in candidates if pkg.price <= 50]
            reasoning_steps.append(f"  预算较低（≤50元），筛选出：{[p.name for p in candidates]}")
        elif needs["budget"] == "高":
            candidates = [pkg for pkg in candidates if pkg.price >= 99]
            reasoning_steps.append(f"  预算较高（≥99元），筛选出：{[p.name for p in candidates]}")
        else:
            reasoning_steps.append(f"  预算中等，保留：{[p.name for p in candidates]}")
        
        # 步骤3：根据流量需求筛选
        reasoning_steps.append("\n【步骤3】根据流量需求筛选套餐")
        if needs["data_need"] == "高":
            # 优先选择流量大的套餐
            candidates.sort(key=lambda p: self._parse_data(p.data), reverse=True)
            reasoning_steps.append(f"  流量需求高，按流量排序：{[p.name for p in candidates[:3]]}")
        elif needs["data_need"] == "低":
            # 优先选择流量小的套餐（通常更便宜）
            candidates.sort(key=lambda p: self._parse_data(p.data))
            reasoning_steps.append(f"  流量需求低，按流量排序：{[p.name for p in candidates[:3]]}")
        else:
            reasoning_steps.append(f"  流量需求中等，保留：{[p.name for p in candidates]}")
        
        # 步骤4：根据通话需求调整
        reasoning_steps.append("\n【步骤4】根据通话需求调整推荐")
        if needs["call_need"] == "高":
            candidates.sort(key=lambda p: p.calls, reverse=True)
            reasoning_steps.append(f"  通话需求高，按通话时长排序：{[p.name for p in candidates[:3]]}")
        
        # 步骤5：最终推荐
        if not candidates:
            recommended = self.PACKAGES[0]  # 默认推荐经济卡
            reasoning_steps.append("\n【步骤5】未找到完全匹配的套餐，推荐默认套餐：经济卡")
        else:
            recommended = candidates[0]
            reasoning_steps.append(f"\n【步骤5】最终推荐：{recommended.name}")
        
        # 生成推荐理由
        reasons = []
        if needs["identity"] and needs["identity"] in recommended.target_group:
            reasons.append(f"符合您的{needs['identity']}身份")
        
        if needs["budget"] == "低" and recommended.price <= 50:
            reasons.append(f"价格实惠（{recommended.price}元/月），符合您的预算")
        elif needs["budget"] == "高" and recommended.price >= 99:
            reasons.append(f"高端套餐（{recommended.price}元/月），满足您的需求")
        
        if needs["data_need"] == "高" and self._parse_data(recommended.data) >= 100:
            reasons.append(f"流量充足（{recommended.data}），满足您的使用需求")
        elif needs["data_need"] == "低" and self._parse_data(recommended.data) <= 20:
            reasons.append(f"流量适中（{recommended.data}），避免浪费")
        
        if needs["call_need"] == "高" and recommended.calls >= 500:
            reasons.append(f"通话时长充足（{recommended.calls}分钟/月）")
        
        if not reasons:
            reasons.append("性价比高，适合大多数用户")
        
        return recommended, reasons, reasoning_steps
    
    def _parse_data(self, data_str: str) -> int:
        """解析流量字符串为数字（用于排序）"""
        if "无限" in data_str:
            return 9999
        try:
            return int(data_str)
        except:
            return 0
    
    def _format_response(self, package: TelecomPackage, reasons: List[str], 
                        reasoning_steps: List[str], needs: Dict[str, Any]) -> str:
        """格式化响应输出"""
        response_parts = []
        
        # 如果启用思维链，显示思考过程
        if self.config.get("use_chain_of_thought", True):
            response_parts.append("【思考过程】")
            response_parts.extend(reasoning_steps)
            response_parts.append("")
        
        # 结构化推荐结果
        response_parts.append("【推荐套餐】" + package.name)
        response_parts.append(f"【价格】{package.price}元/月")
        response_parts.append(f"【流量】{package.data} G/月")
        response_parts.append(f"【通话】{package.calls} 分钟/月")
        response_parts.append(f"【适用人群】{package.target_group}")
        response_parts.append("")
        response_parts.append("【推荐理由】")
        for i, reason in enumerate(reasons, 1):
            response_parts.append(f"{i}. {reason}")
        
        # 检查是否需要更多信息
        missing_info = []
        if not needs.get("identity"):
            missing_info.append("身份信息（如：是否为学生、是否60岁以上等）")
        if not needs.get("budget") or needs["budget"] == "中":
            missing_info.append("预算范围")
        if not needs.get("data_need") or needs["data_need"] == "中":
            missing_info.append("流量使用习惯")
        
        if missing_info:
            response_parts.append("")
            response_parts.append("【温馨提示】")
            response_parts.append("为了给您更精准的推荐，建议提供以下信息：")
            for info in missing_info:
                response_parts.append(f"- {info}")
        
        return "\n".join(response_parts)
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理用户输入，返回推荐结果
        
        Args:
            input_data: 包含 'message' 键的字典
            
        Returns:
            包含 'response' 和 'recommendation' 的字典
        """
        try:
            self.set_state("working")
            user_message = input_data.get("message", "")
            
            if not user_message:
                return {
                    "success": False,
                    "response": "您好！我是智能客服，可以帮您推荐合适的电信套餐。请告诉我您的需求，比如您的身份、预算、流量和通话需求等。",
                    "recommendation": None
                }
            
            # 分析用户需求（思维链推理）
            needs = self._analyze_user_needs(user_message)
            
            # 推荐套餐
            recommended_package, reasons, reasoning_steps = self._recommend_package(needs)
            
            # 格式化响应
            response = self._format_response(recommended_package, reasons, reasoning_steps, needs)
            
            # 保存对话历史
            self.conversation_history.append({
                "user": user_message,
                "assistant": response,
                "timestamp": datetime.now().isoformat()
            })
            
            # 限制历史长度
            max_history = self.config.get("max_memory", 50)
            if len(self.conversation_history) > max_history:
                self.conversation_history = self.conversation_history[-max_history:]
            
            # 添加到记忆
            self.add_to_memory({
                "type": "recommendation",
                "user_message": user_message,
                "recommended_package": recommended_package.name,
                "needs": needs
            })
            
            result = {
                "success": True,
                "response": response,
                "recommendation": {
                    "package": recommended_package.to_dict(),
                    "reasons": reasons,
                    "needs_analysis": needs
                }
            }
            
            self.set_state("idle")
            return result
            
        except Exception as e:
            logger.error(f"处理用户消息时出错: {e}", exc_info=True)
            self.set_state("error")
            return {
                "success": False,
                "response": f"抱歉，处理您的请求时出现了错误：{str(e)}",
                "recommendation": None
            }
    
    def reset(self):
        """重置对话历史"""
        super().reset()
        self.conversation_history = []
        logger.info(f"{self.name} 对话历史已清空")

