# RAG (Retrieval-Augmented Generation) 系统

这是一个基于检索增强生成的文档处理系统，用于处理、索引和查询文档内容。

## 系统架构

系统包含三个主要组件：

1. **文档处理器 (DocumentProcessor)**
   - 支持多种文档格式（txt、pdf、docx）
   - 文本预处理和清洗
   - 智能文本分块

2. **向量处理器 (EmbeddingProcessor)**
   - 文本向量化
   - FAISS 索引构建
   - 向量存储和检索

3. **查询处理器 (QueryProcessor)**
   - 查询向量化
   - 相似度搜索
   - 结果格式化

## 处理流程

### 1. 文档处理阶段 [01-document_processor.py]
```python
# 初始化文档处理器
processor = DocumentProcessor()

# 处理文档目录
chunks = list(processor.process_directory("./data"))
```

处理步骤：
1. 加载文档
2. 文本预处理（清理、标准化）
3. 智能分块（保持语义完整性）
4. 输出文本块

### 2. 向量化阶段 [02-embedding_processor.py]
```python
# 初始化向量处理器
emb_processor = EmbeddingProcessor()

# 创建向量
embeddings = emb_processor.create_embeddings(chunks)

# 构建索引
emb_processor.build_faiss_index(embeddings, chunks)
```

处理步骤：
1. 文本块向量化
2. 构建 FAISS 索引
3. 保存索引和元数据

### 3. 查询阶段 [03-query_processor.py]
```python
# 初始化查询处理器
query_processor = QueryProcessor(emb_processor)

# 执行查询
results = query_processor.search("查询内容")
```

处理步骤：
1. 查询文本向量化
2. 相似度搜索
3. 结果排序和格式化

### 4. 主程序 [4-main.py]
```python
# 主程序入口
if __name__ == "__main__":
    process_documents()
```

处理步骤：
1. 设置目录结构
2. 初始化处理器
3. 执行文档处理
4. 保存处理结果

## 目录结构

```
02-Rag-Demo/
├── data/               # 原始文档目录
├── dist/              # 处理结果目录
├── 01-document_processor.py  # 文档处理模块
├── 02-embedding_processor.py # 向量处理模块
├── 03-query_processor.py    # 查询处理模块
└── 4-main.py            # 主程序
```

## 使用示例

1. 准备文档：
   - 将文档放入 `data` 目录
   - 支持 txt、pdf、docx 格式

2. 运行处理：
```bash
python 4-main.py
```

3. 查看结果：
   - 处理后的文本块保存在 `dist/processed_chunks.txt`
   - 向量索引保存在 `dist/index.*` 文件

## 配置说明

1. 环境变量：
   - 在 `.env` 文件中配置 API 密钥
   - 设置向量模型参数

2. 处理参数：
   - 文本块大小
   - 重叠大小
   - 相似度阈值

## 注意事项

1. 确保安装了所有依赖：
```bash
pip install openai python-dotenv numpy faiss-cpu tqdm python-docx PyPDF2
```

2. 文档处理：
   - 大文档会自动分块
   - 保持句子完整性
   - 处理特殊字符和格式

3. 向量化：
   - 使用 OpenAI 的 embedding 模型
   - 支持批量处理
   - 自动处理 API 限制

4. 查询：
   - 支持自然语言查询
   - 返回相似度分数
   - 可配置返回结果数量