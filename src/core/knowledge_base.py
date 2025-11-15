"""知识库管理"""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)


class KnowledgeBase:
    """知识库管理类"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化知识库
        
        Args:
            config: 配置字典
        """
        self.config = config
        self.vector_store = None
        self.knowledge_graph = None
        self.document_store = None
        self._initialize()
    
    def _initialize(self):
        """初始化各个存储"""
        try:
            # 初始化向量存储
            import chromadb
            client = chromadb.Client()
            collection_name = self.config.get("vector_collection", "knowledge")
            try:
                self.vector_store = client.get_collection(collection_name)
            except:
                self.vector_store = client.create_collection(collection_name)
        except Exception as e:
            logger.warning(f"向量存储初始化失败: {e}")
        
        try:
            # 初始化知识图谱
            import networkx as nx
            self.knowledge_graph = nx.DiGraph()
        except Exception as e:
            logger.warning(f"知识图谱初始化失败: {e}")
        
        # 初始化文档存储
        self.document_store = {"documents": []}
    
    def add_document(self, content: str, metadata: Dict[str, Any] = None):
        """
        添加文档
        
        Args:
            content: 文档内容
            metadata: 元数据
        """
        if metadata is None:
            metadata = {}
        
        # 添加到文档存储
        self.document_store["documents"].append({
            "content": content,
            "metadata": metadata
        })
        
        # 添加到向量存储
        if self.vector_store:
            try:
                from sentence_transformers import SentenceTransformer
                model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
                embedding = model.encode(content).tolist()
                
                self.vector_store.add(
                    embeddings=[embedding],
                    documents=[content],
                    metadatas=[metadata],
                    ids=[f"doc_{len(self.document_store['documents'])}"]
                )
            except Exception as e:
                logger.warning(f"向量存储添加失败: {e}")
    
    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        搜索知识
        
        Args:
            query: 查询字符串
            top_k: 返回结果数量
            
        Returns:
            搜索结果
        """
        results = []
        
        # 向量搜索
        if self.vector_store:
            try:
                from sentence_transformers import SentenceTransformer
                model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
                query_embedding = model.encode(query).tolist()
                
                vector_results = self.vector_store.query(
                    query_embeddings=[query_embedding],
                    n_results=top_k
                )
                
                if vector_results.get("documents"):
                    for i, doc in enumerate(vector_results["documents"][0]):
                        results.append({
                            "content": doc,
                            "source": "vector_store",
                            "score": 1.0 - (vector_results.get("distances", [[1.0]])[0][i] if vector_results.get("distances") else 1.0)
                        })
            except Exception as e:
                logger.warning(f"向量搜索失败: {e}")
        
        # 关键词搜索
        for doc in self.document_store["documents"]:
            if query.lower() in doc["content"].lower():
                results.append({
                    "content": doc["content"],
                    "source": "document_store",
                    "score": 0.8
                })
        
        # 排序
        results.sort(key=lambda x: x.get("score", 0), reverse=True)
        
        return results[:top_k]

