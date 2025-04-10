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


"""
本模块负责将文本块转换为向量，并构建向量索引。

   输入文件 → 读取文本块 → 创建向量 → 构建索引 → 保存结果
"""


class EmbeddingProcessor:
    def __init__(self, model: str = "text-embedding-v3", dimension: int = 1024):
        """初始化向量化处理器

        初始化向量化处理器，设置模型和向量维度。
        从环境变量加载 OpenAI API 配置。

        Args:
            model: 使用的向量模型名称，默认为 "text-embedding-v3"
            dimension: 向量维度，默认为 1024
        """
        load_dotenv()
        self.client = OpenAI(
            api_key=os.getenv("ALIYUN_API_KEY"), base_url=os.getenv("ALIYUN_BASE_URL")
        )
        self.model = model
        self.dimension = dimension
        self.index = None
        self.texts = []
        self.metadata = []

    def create_embeddings(
        self, texts: List[str], batch_size: int = 10
    ) -> List[np.ndarray]:
        """批量创建文本向量

        批量处理文本列表，将每个文本转换为向量。
        使用批处理来提高效率，并添加延迟以避免 API 限制。

        Args:
            texts: 要向量化的文本列表
            batch_size: 每批处理的文本数量，默认为 10

        Returns:
            List[np.ndarray]: 文本向量列表
        """
        embeddings = []
        for i in tqdm(range(0, len(texts), batch_size), desc="创建向量"):
            batch = texts[i : i + batch_size]
            try:
                response = self.client.embeddings.create(model=self.model, input=batch)
                batch_embeddings = [np.array(item.embedding) for item in response.data]
                embeddings.extend(batch_embeddings)
                time.sleep(0.1)  # 避免API限制
            except Exception as e:
                print(f"处理批次 {i//batch_size + 1} 时出错: {str(e)}")
                embeddings.extend([None] * len(batch))
        return embeddings

    def build_faiss_index(
        self,
        embeddings: List[np.ndarray],
        texts: List[str],
        metadata: List[Dict[str, Any]],
    ):
        """构建FAISS索引

        使用 FAISS 构建向量索引，支持快速相似度搜索。
        过滤掉无效的向量，确保索引质量。

        Args:
            embeddings: 向量列表
            texts: 对应的文本列表
            metadata: 文本的元数据列表

        Raises:
            ValueError: 输入列表长度不匹配或没有有效向量时抛出
        """
        if len(embeddings) != len(texts) or len(embeddings) != len(metadata):
            raise ValueError("输入列表长度不匹配")

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

        embeddings_array = np.array(valid_embeddings).astype("float32")

        if embeddings_array.shape[1] != self.dimension:
            raise ValueError(
                f"向量维度不匹配: 期望 {self.dimension}, 实际 {embeddings_array.shape[1]}"
            )

        self.index = faiss.IndexFlatL2(self.dimension)
        self.index.add(embeddings_array)
        self.texts = valid_texts
        self.metadata = valid_metadata

    def save_index(self, save_path: str):
        """保存FAISS索引和相关数据

        将 FAISS 索引和相关的文本、元数据保存到文件。
        使用 pickle 序列化文本和元数据。

        Args:
            save_path: 保存路径（不包含扩展名）

        Raises:
            ValueError: 索引未构建时抛出
        """
        if self.index is None:
            raise ValueError("没有可保存的索引")

        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        faiss.write_index(self.index, f"{save_path}.index")

        data = {
            "texts": self.texts,
            "metadata": self.metadata
        }

        with open(f"{save_path}.data", 'wb') as f:
            pickle.dump(data, f)

    def load_index(self, load_path: str):
        """加载FAISS索引和相关数据

        从文件加载 FAISS 索引和相关的文本、元数据。

        Args:
            load_path: 加载路径（不包含扩展名）

        Raises:
            FileNotFoundError: 索引文件不存在时抛出
        """
        index_file = f"{load_path}.index"
        data_file = f"{load_path}.data"
        
        if not os.path.exists(index_file) or not os.path.exists(data_file):
            raise FileNotFoundError(f"索引文件不存在: {load_path}")
            
        self.index = faiss.read_index(index_file)

        with open(data_file, 'rb') as f:
            data = pickle.load(f)
            self.texts = data["texts"]
            self.metadata = data["metadata"]

    def process_directory_and_save(
        self, input_file: str, output_dir: str, batch_size: int = 10
    ) -> str:
        """处理目录下的所有文档并保存向量索引

        完整的文档处理流程：
        1. 读取处理后的文本块
        2. 创建文本向量
        3. 构建 FAISS 索引
        4. 保存索引和相关数据

        Args:
            input_file: 输入文件路径（处理后的文本块文件）
            output_dir: 输出目录
            batch_size: 批量处理大小，默认为 10

        Returns:
            str: 索引文件路径
        """
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)

        # 读取文本块
        print("\n读取文本块...")
        with open(input_file, "r", encoding="utf-8") as f:
            chunks = [
                line.strip()
                for line in f
                if line.strip() and not line.startswith("===")
            ]
        print(f"✓ 读取完成，共 {len(chunks)} 个文本块")

        # 创建向量
        print("\n创建向量...")
        embeddings = self.create_embeddings(chunks, batch_size)
        print(f"✓ 向量创建完成，共 {len(embeddings)} 个向量")

        # 构建索引
        print("\n构建索引...")
        # 为每个文本块创建简单的元数据
        metadata = [{"source": input_file, "chunk_id": i} for i in range(len(chunks))]
        self.build_faiss_index(embeddings, chunks, metadata)
        print("✓ 索引构建完成")

        # 保存索引
        index_path = os.path.join(output_dir, "index")
        self.save_index(index_path)
        print(f"✓ 索引已保存到: {index_path}")

        return index_path
