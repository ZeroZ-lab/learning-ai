from openai import OpenAI
from dotenv import load_dotenv
import os
from typing import List, Tuple, Dict, Any, Optional
import numpy as np
import json
from tqdm import tqdm
import time
import faiss
import pickle

class EmbeddingProcessor:
    """
    02-01: 向量化处理器
    使用阿里云API进行文本向量化，FAISS进行向量存储和检索
    """
    def __init__(self, model: str = "text-embedding-v3", dimension: int = 1536):
        """
        初始化向量化处理器
        
        Args:
            model (str): 使用的模型名称
            dimension (int): 向量维度
        """
        load_dotenv()
        self.client = OpenAI(
            api_key=os.getenv("ALIYUN_API_KEY"),
            base_url=os.getenv("ALIYUN_BASE_URL")
        )
        self.model = model
        self.dimension = dimension
        self.index = None
        self.texts = []
        self.metadata = []
        
    def create_embedding(self, text: str) -> np.ndarray:
        """
        02-02: 创建单个文本的向量
        
        Args:
            text (str): 输入文本
            
        Returns:
            np.ndarray: 文本向量
        """
        try:
            response = self.client.embeddings.create(
                model=self.model,
                input=text
            )
            return np.array(response.data[0].embedding)
        except Exception as e:
            print(f"创建向量时出错: {str(e)}")
            return None
            
    def create_embeddings(self, texts: List[str], batch_size: int = 10) -> List[np.ndarray]:
        """
        02-03: 批量创建文本向量
        
        Args:
            texts (List[str]): 文本列表
            batch_size (int): 批处理大小
            
        Returns:
            List[np.ndarray]: 向量列表
        """
        embeddings = []
        for i in tqdm(range(0, len(texts), batch_size), desc="创建向量"):
            batch = texts[i:i+batch_size]
            try:
                response = self.client.embeddings.create(
                    model=self.model,
                    input=batch
                )
                batch_embeddings = [np.array(item.embedding) for item in response.data]
                embeddings.extend(batch_embeddings)
                # 添加延迟以避免API限制
                time.sleep(0.1)
            except Exception as e:
                print(f"处理批次 {i//batch_size + 1} 时出错: {str(e)}")
                # 出错时添加None占位
                embeddings.extend([None] * len(batch))
        return embeddings
        
    def build_faiss_index(self, embeddings: List[np.ndarray], texts: List[str], 
                         metadata: List[Dict[str, Any]]):
        """
        02-07: 构建FAISS索引
        
        Args:
            embeddings (List[np.ndarray]): 向量列表
            texts (List[str]): 文本列表
            metadata (List[Dict[str, Any]]): 元数据列表
        """
        # 过滤掉无效的向量
        valid_embeddings = []
        valid_texts = []
        valid_metadata = []
        
        for emb, text, meta in zip(embeddings, texts, metadata):
            if emb is not None:
                valid_embeddings.append(emb)
                valid_texts.append(text)
                valid_metadata.append(meta)
        
        if not valid_embeddings:
            raise ValueError("没有有效的向量可以构建索引")
            
        # 转换为numpy数组
        embeddings_array = np.array(valid_embeddings).astype('float32')
        
        # 创建FAISS索引
        self.index = faiss.IndexFlatL2(self.dimension)
        self.index.add(embeddings_array)
        
        # 保存文本和元数据
        self.texts = valid_texts
        self.metadata = valid_metadata
        
    def search_similar(self, query: str, k: int = 5) -> List[Tuple[str, float, Dict[str, Any]]]:
        """
        02-08: 搜索相似文本
        
        Args:
            query (str): 查询文本
            k (int): 返回最相似的k个结果
            
        Returns:
            List[Tuple[str, float, Dict[str, Any]]]: 
                (文本, 相似度得分, 元数据)列表
        """
        if self.index is None:
            raise ValueError("请先构建FAISS索引")
            
        # 获取查询向量
        query_embedding = self.create_embedding(query)
        if query_embedding is None:
            return []
            
        # 转换为numpy数组
        query_array = np.array([query_embedding]).astype('float32')
        
        # 搜索最相似的k个向量
        distances, indices = self.index.search(query_array, k)
        
        # 返回结果
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.texts):  # 确保索引有效
                results.append((
                    self.texts[idx],
                    1.0 / (1.0 + distances[0][i]),  # 将距离转换为相似度
                    self.metadata[idx]
                ))
                
        return results
        
    def save_index(self, save_path: str):
        """
        02-09: 保存FAISS索引和相关数据
        
        Args:
            save_path (str): 保存路径
        """
        if self.index is None:
            raise ValueError("没有可保存的索引")
            
        # 确保目录存在
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # 保存FAISS索引
        faiss.write_index(self.index, f"{save_path}.index")
        
        # 保存文本和元数据
        data = {
            "texts": self.texts,
            "metadata": self.metadata
        }
        
        with open(f"{save_path}.data", 'wb') as f:
            pickle.dump(data, f)
            
    def load_index(self, load_path: str):
        """
        02-10: 加载FAISS索引和相关数据
        
        Args:
            load_path (str): 加载路径
        """
        # 加载FAISS索引
        self.index = faiss.read_index(f"{load_path}.index")
        
        # 加载文本和元数据
        with open(f"{load_path}.data", 'rb') as f:
            data = pickle.load(f)
            self.texts = data["texts"]
            self.metadata = data["metadata"]

# 测试代码
if __name__ == "__main__":
    # 创建处理器实例
    processor = EmbeddingProcessor()
    
    # 测试单个文本向量化
    test_text = "这是一个测试文本"
    embedding = processor.create_embedding(test_text)
    print(f"单个文本向量维度: {len(embedding) if embedding is not None else 0}")
    
    # 测试批量向量化
    test_texts = [
        "这是第一个测试文本",
        "这是第二个测试文本",
        "这是第三个测试文本"
    ]
    embeddings = processor.create_embeddings(test_texts)
    print(f"批量处理向量数量: {len(embeddings)}")
    
    # 构建FAISS索引
    metadata = [{"source": f"test_{i}"} for i in range(len(test_texts))]
    processor.build_faiss_index(embeddings, test_texts, metadata)
    
    # 测试相似度搜索
    query = "测试文本"
    results = processor.search_similar(query, k=2)
    print("\n相似度搜索结果:")
    for text, score, meta in results:
        print(f"文本: {text}")
        print(f"相似度: {score:.4f}")
        print(f"元数据: {meta}")
        print()
    
    # 测试保存和加载索引
    save_path = "./07-Rag/data/embeddings"
    processor.save_index(save_path)
    
    # 创建新的处理器实例并加载索引
    new_processor = EmbeddingProcessor()
    new_processor.load_index(save_path)
    
    # 验证加载的索引
    new_results = new_processor.search_similar(query, k=2)
    print("\n加载后的相似度搜索结果:")
    for text, score, meta in new_results:
        print(f"文本: {text}")
        print(f"相似度: {score:.4f}")
        print(f"元数据: {meta}")
        print() 