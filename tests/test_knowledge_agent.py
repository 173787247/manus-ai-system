"""测试知识检索智能体"""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agents.knowledge_agent import KnowledgeAgent


def test_knowledge_agent_initialization():
    """测试知识检索智能体初始化"""
    config = {
        "vector_collection": "test_knowledge"
    }
    
    agent = KnowledgeAgent(config)
    
    assert agent.name == "KnowledgeAgent"
    assert agent.state == "idle"


def test_knowledge_agent_retrieve():
    """测试知识检索"""
    config = {"vector_collection": "test"}
    agent = KnowledgeAgent(config)
    
    result = agent.retrieve("测试查询", top_k=3)
    
    # 验证返回结构
    assert "status" in result
    assert "query" in result
    assert "results" in result
    assert isinstance(result["results"], list)


def test_knowledge_agent_merge_results():
    """测试结果融合"""
    config = {"vector_collection": "test"}
    agent = KnowledgeAgent(config)
    
    results = [
        {"content": "内容1", "source": "vector", "score": 0.9},
        {"content": "内容1", "source": "keyword", "score": 0.8},  # 重复
        {"content": "内容2", "source": "kg", "score": 0.7}
    ]
    
    merged = agent._merge_results(results)
    
    # 应该去重
    assert len(merged) <= len(results)
    assert len(merged) >= 2  # 至少保留2个不同的结果


def test_knowledge_agent_rerank():
    """测试结果重排序"""
    config = {"vector_collection": "test"}
    agent = KnowledgeAgent(config)
    
    results = [
        {"content": "内容1", "score": 0.7},
        {"content": "内容2", "score": 0.9},
        {"content": "内容3", "score": 0.5}
    ]
    
    reranked = agent._rerank(results, "查询")
    
    # 应该按分数降序排列
    assert reranked[0]["score"] >= reranked[1]["score"]
    assert reranked[1]["score"] >= reranked[2]["score"]

