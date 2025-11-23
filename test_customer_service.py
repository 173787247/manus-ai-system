"""测试智能客服系统"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.agents.customer_service_agent import CustomerServiceAgent
import json


def test_customer_service():
    """测试智能客服系统"""
    print("=" * 80)
    print("测试基于 RASCEF 框架的智能客服系统")
    print("=" * 80)
    print()
    
    # 创建 Agent
    agent = CustomerServiceAgent(
        name="测试客服",
        config={
            "use_chain_of_thought": True,
            "max_memory": 10
        }
    )
    
    # 测试用例
    test_cases = [
        {
            "name": "测试用例1：在校大学生",
            "message": "我是大学生，平时用流量比较多，看视频和玩游戏，预算有限"
        },
        {
            "name": "测试用例2：60岁以上老人",
            "message": "我60多岁了，平时不怎么用手机，就是偶尔打个电话，想要最便宜的"
        },
        {
            "name": "测试用例3：高端用户",
            "message": "我需要无限流量，经常打电话，预算不是问题"
        },
        {
            "name": "测试用例4：普通用户",
            "message": "我是普通上班族，平时用手机看看新闻，偶尔打电话"
        },
        {
            "name": "测试用例5：信息不足",
            "message": "我想办个套餐"
        }
    ]
    
    # 执行测试
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'=' * 80}")
        print(f"【{test_case['name']}】")
        print(f"{'=' * 80}")
        print(f"\n用户输入：{test_case['message']}")
        print("\n" + "-" * 80)
        
        result = agent.process({"message": test_case["message"]})
        
        if result["success"]:
            print(result["response"])
            
            if result.get("recommendation"):
                print("\n" + "-" * 80)
                print("推荐详情（JSON格式）：")
                print(json.dumps(result["recommendation"], ensure_ascii=False, indent=2))
        else:
            print(f"错误：{result['response']}")
        
        print()
    
    # 显示 Agent 状态
    print("=" * 80)
    print("Agent 状态信息")
    print("=" * 80)
    status = agent.get_status()
    print(json.dumps(status, ensure_ascii=False, indent=2))
    print()
    
    print("测试完成！")


if __name__ == "__main__":
    test_customer_service()

