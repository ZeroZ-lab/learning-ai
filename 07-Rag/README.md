# RAG System

一个基于检索增强生成（RAG）的文档处理系统。

## 功能特点

- 支持多种文档格式（txt, pdf, docx）
- 高效的文档分块处理
- 基于 OpenAI 的文本向量化
- 使用 FAISS 进行向量存储和检索
- 模块化设计，易于扩展

## 安装

```bash
pip install -e .
```

## 使用流程

1. 文档处理
```python
from src.document_processor import DocumentProcessor

processor = DocumentProcessor()
chunks = processor.process_directory("path/to/documents")
```

2. 向量化处理
```python
from src.embedding_processor import EmbeddingProcessor

processor = EmbeddingProcessor()
embeddings = processor.create_embeddings(chunks)
processor.build_faiss_index(embeddings, chunks)
```

3. 查询处理
```python
from src.query_processor import QueryProcessor

processor = QueryProcessor()
results = processor.search("your query", k=5)
```

## 项目结构

```
rag-system/
├── src/
│   ├── document_processor.py
│   ├── embedding_processor.py
│   └── query_processor.py
├── tests/
├── data/
├── setup.py
└── README.md
``` 