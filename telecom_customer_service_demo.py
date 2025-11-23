"""电信套餐推荐智能客服演示程序"""
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.agents.customer_service_agent import CustomerServiceAgent
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def print_separator():
    """打印分隔线"""
    print("=" * 80)


def main():
    """主函数"""
    print_separator()
    print("欢迎使用基于 RASCEF 框架的智能客服系统 - 电信套餐推荐")
    print_separator()
    print()
    print("系统特点：")
    print("1. 使用 RASCEF 框架构建 Prompt")
    print("2. 采用思维链（Chain of Thought）推理")
    print("3. 结构化输出推荐结果")
    print()
    print("可用套餐：")
    print("- 经济卡：29元/月，20G流量，100分钟通话")
    print("- 关爱卡：9元/月，5G流量，10分钟通话（60岁以上）")
    print("- 校园卡：39元/月，200G流量，100分钟通话（在校生）")
    print("- 无限卡：199元/月，无限流量，500分钟通话")
    print("- 精英卡：99元/月，200G流量，500分钟通话")
    print()
    print("输入 'quit' 或 'exit' 退出程序")
    print("输入 'reset' 清空对话历史")
    print_separator()
    print()
    
    # 创建智能客服 Agent
    agent = CustomerServiceAgent(
        name="智能客服",
        config={
            "model": "gpt-4",
            "temperature": 0.7,
            "max_memory": 50,
            "use_chain_of_thought": True
        }
    )
    
    print("智能客服：您好！我是智能客服，可以帮您推荐合适的电信套餐。")
    print("请告诉我您的需求，比如您的身份、预算、流量和通话需求等。")
    print()
    
    while True:
        try:
            # 获取用户输入
            user_input = input("您：").strip()
            
            if not user_input:
                continue
            
            # 处理退出命令
            if user_input.lower() in ['quit', 'exit', '退出']:
                print("\n感谢使用智能客服系统，再见！")
                break
            
            # 处理重置命令
            if user_input.lower() in ['reset', '重置']:
                agent.reset()
                print("\n对话历史已清空。")
                print()
                continue
            
            # 处理用户消息
            print()
            print_separator()
            result = agent.process({"message": user_input})
            
            if result["success"]:
                print(result["response"])
            else:
                print(f"错误：{result['response']}")
            
            print_separator()
            print()
            
        except KeyboardInterrupt:
            print("\n\n程序已中断，再见！")
            break
        except Exception as e:
            logger.error(f"处理输入时出错: {e}", exc_info=True)
            print(f"\n抱歉，发生了错误：{str(e)}")
            print()


if __name__ == "__main__":
    main()

