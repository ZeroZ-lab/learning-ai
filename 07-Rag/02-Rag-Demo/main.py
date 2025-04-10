import os
from document_processor import DocumentProcessor
from embedding_processor import EmbeddingProcessor
from query_processor import QueryProcessor
from rerank_processor import RerankProcessor
from generation_processor import GenerationProcessor
from datetime import datetime
import dashscope
from dotenv import load_dotenv

load_dotenv()
dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")


class RagProcessor:
    def __init__(self):
        """初始化RAG处理器"""
        self.base_dir = os.path.dirname(__file__)
        self.doc_dir = os.path.join(self.base_dir, "data")
        self.output_dir = os.path.join(self.base_dir, "dist")
        self.processed_file = os.path.join(self.output_dir, "processed_chunks.txt")
        self.index_path = os.path.join(self.output_dir, "index")
        print("\n=== RAG 系统初始化 ===")
        print(f"文档目录: {self.doc_dir}")
        print(f"输出目录: {self.output_dir}")
        print("=" * 50)

    def process_documents(self) -> str:
        """第一步：文档预处理

        Returns:
            str: 处理后的文件路径
        """
        print("\n=== 第一步：文档预处理 ===")
        start_time = datetime.now()
        doc_processor = DocumentProcessor()
        result = doc_processor.process_directory_and_save(self.doc_dir, self.output_dir)
        duration = (datetime.now() - start_time).total_seconds()
        print(f"文档预处理完成，耗时: {duration:.2f}秒")
        print("=" * 50)
        return result

    def create_embeddings(self, processed_file: str = None) -> str:
        """第二步：向量化处理

        Args:
            processed_file: 处理后的文件路径，如果为None则使用默认路径

        Returns:
            str: 索引文件路径
        """
        print("\n=== 第二步：向量化处理 ===")
        if not processed_file:
            processed_file = self.processed_file

        if not os.path.exists(processed_file):
            print(f"文件不存在: {processed_file}")
            print("请先运行文档预处理步骤")
            print("=" * 50)
            return None

        start_time = datetime.now()
        emb_processor = EmbeddingProcessor()
        result = emb_processor.process_directory_and_save(
            processed_file, self.output_dir
        )
        duration = (datetime.now() - start_time).total_seconds()
        print(f"向量化处理完成，耗时: {duration:.2f}秒")
        print("=" * 50)
        return result

    def query_documents(self, index_path: str = None, queries: list = None):
        """第三步：查询处理

        Args:
            index_path: 索引文件路径，如果为None则使用默认路径
            queries: 查询列表，如果为None则使用默认查询
        """
        print("\n=== 第三步：查询处理 ===")
        if not index_path:
            index_path = self.index_path

        if not os.path.exists(f"{index_path}.index"):
            print(f"索引文件不存在: {index_path}.index")
            print("请先运行向量化处理步骤")
            print("=" * 50)
            return

        try:
            # 初始化向量处理器和查询处理器
            emb_processor = EmbeddingProcessor()
            emb_processor.load_index(index_path)
            query_processor = QueryProcessor(emb_processor)

            # 执行查询
            print("\n执行查询...")
            for query in queries:
                print(f"\n查询: {query}")
                start_time = datetime.now()
                results = query_processor.search(query)
                duration = (datetime.now() - start_time).total_seconds()
                print(f"检索完成，耗时: {duration:.2f}秒")
                print(query_processor.format_results(results))

                # 初始化重排序器
                reranker = RerankProcessor()

                # 对检索结果进行重排序
                print("\n开始重排序...")
                start_time = datetime.now()
                reranked_results = reranker.rerank(query, results)
                duration = (datetime.now() - start_time).total_seconds()
                print(f"重排序完成，耗时: {duration:.2f}秒")
                print(reranker.format_results(reranked_results))

                return reranked_results

        except Exception as e:
            print(f"查询处理出错: {str(e)}")
            print("请确保索引文件完整且格式正确")
            print("=" * 50)
            return None


def main():
    """主函数，可以选择运行全部步骤或单个步骤"""
    print("\n=== RAG 系统启动 ===")
    start_time = datetime.now()

    rag = RagProcessor()

    # 单独运行某一步
    # rag.process_documents()  # 只运行文档处理
    # rag.create_embeddings()  # 只运行向量化处理

    # 运行查询处理
    query = "介绍西湖"
    reranked_results = rag.query_documents(rag.index_path, [query])

    if reranked_results:
        # 初始化生成处理器
        generator = GenerationProcessor()

        # 模型生成
        print("\n=== 第四步：模型生成 ===")
        start_time = datetime.now()
        response = generator.generate_response(query, reranked_results)
        duration = (datetime.now() - start_time).total_seconds()
        print(f"生成完成，耗时: {duration:.2f}秒")
        print("\n生成结果:")
        print(response)
        print("=" * 50)

    duration = (datetime.now() - start_time).total_seconds()
    print(f"\n=== RAG 系统运行完成，总耗时: {duration:.2f}秒 ===")


if __name__ == "__main__":
    main()
