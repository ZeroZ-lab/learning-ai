from typing import List, Dict, Any
from embedding_processor import EmbeddingProcessor


class QueryProcessor:
    def __init__(self, embedding_processor: EmbeddingProcessor):
        """初始化查询处理器
        
        Args:
            embedding_processor: 已经训练好的向量处理器实例
        """
        self.embedding_processor = embedding_processor

    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """执行查询并返回结果
        
        Args:
            query: 查询文本
            k: 返回的最相似文本数量
            
        Returns:
            List[Dict[str, Any]]: 查询结果列表，每个结果包含文本、相似度和元数据
        """
        # 创建查询向量
        query_embedding = self.embedding_processor.create_embeddings([query])[0]
        if query_embedding is None:
            return []
        
        # 使用FAISS搜索
        distances, indices = self.embedding_processor.index.search(
            query_embedding.reshape(1, -1).astype('float32'), 
            k
        )
        
        # 格式化结果
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.embedding_processor.texts):
                results.append({
                    "text": self.embedding_processor.texts[idx],
                    "similarity": 1.0 / (1.0 + distances[0][i]),
                    "metadata": self.embedding_processor.metadata[idx]
                })
        
        return results

    def format_results(self, results: List[Dict[str, Any]]) -> str:
        """格式化查询结果
        
        Args:
            results: 查询结果列表
            
        Returns:
            str: 格式化后的结果字符串
        """
        if not results:
            return "没有找到相关结果"
            
        output = []
        for i, result in enumerate(results, 1):
            output.append(f"结果 {i}:")
            output.append(f"相似度: {result['similarity']:.4f}")
            output.append(f"内容: {result['text']}")
            if result['metadata']:
                output.append(f"元数据: {result['metadata']}")
            output.append("-" * 50)
            
        return "\n".join(output) 