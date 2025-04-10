import os
from typing import List, Union, Generator
import re
from docx import Document
from PyPDF2 import PdfReader
from tqdm import tqdm
import bisect
from multiprocessing import Pool
from functools import partial


class DocumentProcessor:
    def __init__(self):
        """初始化文档处理器
        
        初始化文档处理器，准备处理各种格式的文档。
        目前支持 txt、pdf、docx 格式的文档。
        """
        pass

    def load_document(self, file_path: str) -> str:
        """加载文档内容
        
        根据文件扩展名选择合适的方法加载文档内容。
        支持 txt、pdf、docx 格式。
        
        Args:
            file_path: 文档文件路径
            
        Returns:
            str: 文档的文本内容
            
        Raises:
            FileNotFoundError: 文件不存在时抛出
            ValueError: 不支持的文件格式时抛出
            RuntimeError: 文件加载失败时抛出
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")

        file_ext = os.path.splitext(file_path)[1].lower()

        try:
            if file_ext == ".txt":
                with open(file_path, "r", encoding="utf-8") as f:
                    return f.read()
            elif file_ext == ".pdf":
                reader = PdfReader(file_path)
                text_parts = []
                for page in reader.pages:
                    text_parts.append(page.extract_text())
                return "".join(text_parts)
            elif file_ext == ".docx":
                doc = Document(file_path)
                return "\n".join([paragraph.text for paragraph in doc.paragraphs])
            else:
                raise ValueError(f"不支持的文件格式: {file_ext}")
        except (IOError, ValueError) as e:
            raise RuntimeError(f"加载文件 {file_path} 失败: {str(e)}")

    def preprocess_text(self, text: str) -> str:
        """文本预处理
        
        对文本进行清理和标准化处理：
        1. 统一换行符
        2. 移除特殊字符
        3. 标准化空白字符
        
        Args:
            text: 原始文本
            
        Returns:
            str: 处理后的文本
        """
        if not text:
            return ""

        text = re.sub(r"[\r\n]+", "\n", text)
        text = re.sub(r"[^\w\s\u4e00-\u9fff]|\s+", " ", text)
        return text.strip()

    def find_sentence_boundaries(self, text: str) -> List[int]:
        """查找句子边界
        
        在文本中查找句子结束的位置，用于智能分块。
        支持的句子结束符：.。!！?？\n
        
        Args:
            text: 要处理的文本
            
        Returns:
            List[int]: 句子边界位置的列表
        """
        boundaries = []
        for i, char in enumerate(text):
            if char in ".。!！?？\n":
                boundaries.append(i)
        return boundaries

    def split_text(
        self, text: str, chunk_size: int = 1000, chunk_overlap: int = 200
    ) -> List[str]:
        """将文本分割成块
        
        将文本分割成指定大小的块，同时保持句子的完整性。
        使用重叠来避免在句子中间分割。
        
        Args:
            text: 要分割的文本
            chunk_size: 每个块的最大字符数
            chunk_overlap: 相邻块之间的重叠字符数
            
        Returns:
            List[str]: 文本块列表
        """
        if not text:
            return []

        boundaries = self.find_sentence_boundaries(text)
        if not boundaries:
            return [
                text[i : i + chunk_size]
                for i in range(0, len(text), chunk_size - chunk_overlap)
            ]

        chunks = []
        start = 0
        text_length = len(text)

        while start < text_length:
            end = min(start + chunk_size, text_length)

            if end < text_length:
                boundary_idx = bisect.bisect_right(boundaries, end) - 1
                if boundary_idx >= 0:
                    end = boundaries[boundary_idx] + 1

            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)

            start = end - chunk_overlap

        return chunks

    def process_single_file(
        self, file_path: str, chunk_size: int, chunk_overlap: int
    ) -> List[str]:
        """处理单个文件
        
        加载、预处理并分割单个文件的内容。
        
        Args:
            file_path: 文件路径
            chunk_size: 文本块大小
            chunk_overlap: 文本块重叠大小
            
        Returns:
            List[str]: 处理后的文本块列表
        """
        try:
            print(f"开始处理文件: {file_path}")
            text = self.load_document(file_path)
            print(f"文件加载完成，开始预处理...")
            text = self.preprocess_text(text)
            print(f"预处理完成，开始分割...")
            chunks = self.split_text(text, chunk_size, chunk_overlap)
            print(f"分割完成，共 {len(chunks)} 个文本块")
            return chunks
        except Exception as e:
            print(f"处理文件 {file_path} 时出错: {str(e)}")
            return []

    def process_directory(
        self, directory_path: str, chunk_size: int = 1000, chunk_overlap: int = 200
    ) -> Generator[str, None, None]:
        """处理整个目录下的文档
        
        并行处理目录下的所有文档，支持 txt、pdf、docx 格式。
        使用多进程加速处理。
        
        Args:
            directory_path: 目录路径
            chunk_size: 文本块大小
            chunk_overlap: 文本块重叠大小
            
        Returns:
            Generator[str, None, None]: 文本块生成器
            
        Raises:
            NotADirectoryError: 目录不存在时抛出
        """
        if not os.path.isdir(directory_path):
            raise NotADirectoryError(f"目录不存在: {directory_path}")

        supported_extensions = (".txt", ".pdf", ".docx")
        files = [
            f
            for f in os.listdir(directory_path)
            if any(f.lower().endswith(ext) for ext in supported_extensions)
        ]

        with Pool() as pool:
            process_func = partial(
                self.process_single_file, chunk_size=chunk_size, chunk_overlap=chunk_overlap
            )

            for chunks in tqdm(
                pool.imap(process_func, [os.path.join(directory_path, f) for f in files]),
                total=len(files),
                desc="处理文档",
            ):
                for chunk in chunks:
                    yield chunk

    def process_directory_and_save(
        self, 
        input_dir: str, 
        output_dir: str, 
        chunk_size: int = 50, 
        chunk_overlap: int = 10
    ) -> str:
        """处理目录下的所有文档并保存结果
        
        处理目录下的所有文档，并将结果保存到指定目录。
        每个文本块都会添加序号标记。
        
        Args:
            input_dir: 输入文档目录
            output_dir: 输出结果目录
            chunk_size: 文本块大小
            chunk_overlap: 文本块重叠大小
            
        Returns:
            str: 输出文件路径
        """
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        
        # 处理文档
        print("\n处理文档...")
        chunks = list(self.process_directory(input_dir, chunk_size, chunk_overlap))
        print(f"✓ 处理完成，共 {len(chunks)} 个文本块")
        
        # 保存结果
        output_file = os.path.join(output_dir, "processed_chunks.txt")
        with open(output_file, "w", encoding="utf-8") as f:
            for i, chunk in enumerate(chunks, 1):
                f.write(f"=== 块 {i} ===\n{chunk}\n\n")
        print(f"✓ 结果已保存到: {output_file}")
        
        return output_file 