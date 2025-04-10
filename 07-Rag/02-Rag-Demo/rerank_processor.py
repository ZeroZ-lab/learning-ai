import dashscope
from http import HTTPStatus
from typing import List, Dict, Tuple
from dotenv import load_dotenv
import os
import numpy as np
from datetime import datetime

load_dotenv()

# 设置 API Key
dashscope.api_key = os.getenv('DASHSCOPE_API_KEY')

class RerankProcessor:
    def __init__(self):
        """初始化重排序处理器，使用阿里云 GTE-Rerank 服务"""
        self.model = dashscope.TextReRank.Models.gte_rerank
        print("\n=== 初始化重排序处理器 ===")
        print(f"模型: {self.model}")
        print("=" * 50)
        
    def rerank(self, query: str, documents: List[str], top_k: int = 5) -> List[Tuple[str, float]]:
        """对文档进行重排序
        
        Args:
            query: 查询文本
            documents: 待排序的文档列表
            top_k: 返回前k个结果
            
        Returns:
            List[Tuple[str, float]]: 排序后的文档列表，每个元素为(文档内容, 相关性分数)
        """
        print("\n=== 开始重排序 ===")
        print(f"查询: {query}")
        print(f"文档数量: {len(documents)}")
        print(f"返回前 {top_k} 个结果")
        print("-" * 50)
        
        try:
            # 确保文档列表中的内容都是字符串类型
            documents = [str(doc) for doc in documents]
            
            start_time = datetime.now()
            resp = dashscope.TextReRank.call(
                model=self.model,
                query=query,
                documents=documents,
                top_n=top_k,
                return_documents=True
            )
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            if resp.status_code == HTTPStatus.OK:
                results = []
                for item in resp.output['results']:
                    # 确保分数是 Python 原生 float 类型
                    score = float(item['relevance_score'])
                    results.append((item['document']['text'], score))
                
                print(f"重排序完成，耗时: {duration:.2f}秒")
                print(f"返回结果数量: {len(results)}")
                print("=" * 50)
                return results
            else:
                print(f"重排序失败: {resp}")
                print("=" * 50)
                return []
                
        except Exception as e:
            print(f"重排序出错: {str(e)}")
            print("=" * 50)
            return []
    
    def rerank_with_metadata(self, query: str, documents: List[Dict], top_k: int = 5) -> List[Dict]:
        """对带有元数据的文档进行重排序
        
        Args:
            query: 查询文本
            documents: 待排序的文档列表，每个文档是一个字典，包含content和其他元数据
            top_k: 返回前k个结果
            
        Returns:
            List[Dict]: 排序后的文档列表，每个文档包含原始元数据和新的相关性分数
        """
        print("\n=== 开始带元数据的重排序 ===")
        print(f"查询: {query}")
        print(f"文档数量: {len(documents)}")
        print(f"返回前 {top_k} 个结果")
        print("-" * 50)
        
        # 提取文档内容
        doc_contents = [str(doc.get('content', '')) for doc in documents]
        
        # 进行重排序
        reranked_pairs = self.rerank(query, doc_contents, top_k)
        
        # 构建结果
        results = []
        for content, score in reranked_pairs:
            # 找到对应的原始文档
            original_doc = next((doc for doc in documents if str(doc.get('content', '')) == content), {})
            # 添加分数并保留原始元数据
            result = original_doc.copy()
            result['score'] = float(score)  # 确保分数是 Python 原生 float 类型
            results.append(result)
            
        print(f"带元数据的重排序完成")
        print(f"返回结果数量: {len(results)}")
        print("=" * 50)
        return results

    def format_results(self, results: List[Dict]) -> str:
        """格式化重排序结果
        
        Args:
            results: 重排序结果列表，可以是字典列表或元组列表
            
        Returns:
            str: 格式化后的结果字符串
        """
        if not results:
            return "没有找到相关结果"
            
        formatted = []
        formatted.append("\n=== 重排序结果 ===")
        
        for i, result in enumerate(results, 1):
            formatted.append(f"\n结果 {i}:")
            
            # 处理元组类型的结果 (content, score)
            if isinstance(result, tuple):
                content, score = result
                formatted.append(f"分数: {float(score):.4f}")
                formatted.append(f"内容: {content}")
            # 处理字典类型的结果
            else:
                score = float(result.get('score', 0))
                formatted.append(f"分数: {score:.4f}")
                formatted.append(f"内容: {result.get('content', '')}")
                if 'metadata' in result:
                    formatted.append(f"元数据: {result['metadata']}")
                    
            formatted.append("-" * 50)
            
        formatted.append("\n=== 结果展示完成 ===")
        return "\n".join(formatted) 