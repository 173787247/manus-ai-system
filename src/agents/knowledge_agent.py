"""知识检索智能体"""
from typing import Dict, Any, List, Optional
import logging

from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


class KnowledgeAgent(BaseAgent):
    """知识检索智能体，负责多源知识检索与融合"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化知识检索智能体
        
        Args:
            config: 配置字典
        """
        super().__init__("KnowledgeAgent", config)
        self.vector_store = self._init_vector_store()
        self.knowledge_graph = self._init_knowledge_graph()
        self.document_store = self._init_document_store()
    
    def _init_vector_store(self):
        """初始化向量数据库"""
        try:
            import chromadb
            client = chromadb.Client()
            collection_name = self.config.get("vector_collection", "knowledge")
            try:
                collection = client.get_collection(collection_name)
            except:
                collection = client.create_collection(collection_name)
            return collection
        except Exception as e:
            logger.warning(f"向量数据库初始化失败: {e}")
            return None
    
    def _init_knowledge_graph(self):
        """初始化知识图谱"""
        try:
            import networkx as nx
            graph = nx.DiGraph()
            return graph
        except Exception as e:
            logger.warning(f"知识图谱初始化失败: {e}")
            return None
    
    def _init_document_store(self):
        """初始化文档存储"""
        # 简化实现
        return {"documents": []}
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理输入数据
        
        Args:
            input_data: 输入数据字典
            
        Returns:
            处理结果
        """
        query = input_data.get("query", "")
        top_k = input_data.get("top_k", 5)
        return self.retrieve(query, top_k)
    
    def retrieve(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        """
        检索知识
        
        Args:
            query: 查询字符串
            top_k: 返回结果数量
            
        Returns:
            检索结果
        """
        self.set_state("working")
        
        try:
            results = []
            
            # 1. 向量检索
            if self.vector_store:
                vector_results = self._vector_search(query, top_k)
                results.extend(vector_results)
            
            # 2. 关键词检索
            keyword_results = self._keyword_search(query, top_k)
            results.extend(keyword_results)
            
            # 3. 知识图谱查询
            if self.knowledge_graph:
                kg_results = self._kg_query(query)
                results.extend(kg_results)
            
            # 4. 结果融合与排序
            merged_results = self._merge_results(results)
            reranked_results = self._rerank(merged_results, query)
            
            self.set_state("idle")
            return {
                "status": "success",
                "query": query,
                "results": reranked_results[:top_k],
                "total": len(reranked_results)
            }
            
        except Exception as e:
            logger.error(f"知识检索失败: {e}")
            self.set_state("error")
            return {
                "status": "error",
                "message": str(e),
                "results": []
            }
    
    def _vector_search(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        """向量搜索"""
        if not self.vector_store:
            return []
        
        try:
            # 生成查询向量（简化实现）
            from sentence_transformers import SentenceTransformer
            model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
            query_embedding = model.encode(query).tolist()
            
            # 搜索
            results = self.vector_store.query(
                query_embeddings=[query_embedding],
                n_results=top_k
            )
            
            # 格式化结果
            formatted_results = []
            if results.get("documents"):
                for i, doc in enumerate(results["documents"][0]):
                    formatted_results.append({
                        "content": doc,
                        "source": "vector_store",
                        "score": results.get("distances", [[1.0]])[0][i] if results.get("distances") else 1.0
                    })
            
            return formatted_results
        except Exception as e:
            logger.warning(f"向量搜索失败: {e}")
            return []
    
    def _keyword_search(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        """关键词搜索"""
        # 简化实现
        results = []
        documents = self.document_store.get("documents", [])
        
        for doc in documents:
            if query.lower() in doc.get("content", "").lower():
                results.append({
                    "content": doc.get("content", ""),
                    "source": "document_store",
                    "score": 1.0
                })
        
        return results[:top_k]
    
    def _kg_query(self, query: str) -> List[Dict[str, Any]]:
        """知识图谱查询"""
        if not self.knowledge_graph:
            return []
        
        results = []
        # 简化实现：查找包含查询关键词的节点
        for node in self.knowledge_graph.nodes():
            if query.lower() in str(node).lower():
                neighbors = list(self.knowledge_graph.neighbors(node))
                for neighbor in neighbors:
                    relation = self.knowledge_graph[node][neighbor].get("relation", "related")
                    results.append({
                        "content": f"{node} {relation} {neighbor}",
                        "source": "knowledge_graph",
                        "score": 0.8
                    })
        
        return results
    
    def _merge_results(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """融合结果"""
        # 去重
        seen = set()
        merged = []
        
        for result in results:
            content = result.get("content", "")[:100]  # 使用前100字符作为ID
            if content not in seen:
                seen.add(content)
                merged.append(result)
        
        return merged
    
    def _rerank(self, results: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
        """重排序"""
        # 简化实现：按分数排序
        return sorted(results, key=lambda x: x.get("score", 0), reverse=True)

