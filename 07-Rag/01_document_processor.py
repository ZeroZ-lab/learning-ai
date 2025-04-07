import os
from typing import List, Union, Generator
import re
from docx import Document
from PyPDF2 import PdfReader
from tqdm import tqdm
import bisect
from multiprocessing import Pool
from functools import partial


def load_document(file_path: str) -> str:
    """
    01-01: 加载文档内容
    支持的文件格式：txt, pdf, docx

    优化点：
    1. 使用列表收集文本片段，避免字符串拼接
    2. 具体化异常类型，提高错误处理效率

    Args:
        file_path (str): 文档路径

    Returns:
        str: 文档内容
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
            # 使用列表收集文本片段，避免字符串拼接
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


def preprocess_text(text: str) -> str:
    """
    01-02: 文本预处理
    优化点：
    1. 合并正则表达式，减少文本遍历次数
    2. 使用更高效的正则表达式模式

    Args:
        text (str): 原始文本

    Returns:
        str: 处理后的文本
    """
    if not text:
        return ""

    # 合并正则表达式，一次性处理换行符和空白字符
    # [\r\n]+ 匹配一个或多个换行符
    # [^\w\s\u4e00-\u9fff] 匹配非单词字符、非空白字符、非中文字符
    # \s+ 匹配一个或多个空白字符
    text = re.sub(r"[\r\n]+", "\n", text)  # 标准化换行符
    text = re.sub(r"[^\w\s\u4e00-\u9fff]|\s+", " ", text)  # 处理特殊字符和空白
    return text.strip()


def find_sentence_boundaries(text: str) -> List[int]:
    """
    预处理句子边界
    优化点：
    1. 预处理句子边界，避免重复查找
    2. 使用列表收集边界位置

    Args:
        text (str): 待处理的文本

    Returns:
        List[int]: 句子边界位置列表
    """
    boundaries = []
    for i, char in enumerate(text):
        if char in ".。!！?？\n":
            boundaries.append(i)
    return boundaries


def split_text(
    text: str, chunk_size: int = 1000, chunk_overlap: int = 200
) -> List[str]:
    """
    01-03: 将文本分割成块
    优化点：
    1. 使用预处理的句子边界
    2. 使用二分查找快速定位边界
    3. 使用列表收集块，避免字符串拼接

    Args:
        text (str): 待分割的文本
        chunk_size (int): 每个块的大小
        chunk_overlap (int): 块之间的重叠大小

    Returns:
        List[str]: 文本块列表
    """
    if not text:
        return []

    # 预处理句子边界
    boundaries = find_sentence_boundaries(text)
    if not boundaries:
        # 如果没有找到句子边界，按固定大小分割
        return [
            text[i : i + chunk_size]
            for i in range(0, len(text), chunk_size - chunk_overlap)
        ]

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)

        # 使用二分查找快速定位最近的句子边界
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
    file_path: str, chunk_size: int, chunk_overlap: int
) -> List[str]:
    """
    处理单个文件
    优化点：
    1. 封装单个文件处理逻辑
    2. 便于并行处理

    Args:
        file_path (str): 文件路径
        chunk_size (int): 块大小
        chunk_overlap (int): 重叠大小

    Returns:
        List[str]: 文本块列表
    """
    try:
        text = load_document(file_path)
        text = preprocess_text(text)
        return split_text(text, chunk_size, chunk_overlap)
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {str(e)}")
        return []


def process_directory(
    directory_path: str, chunk_size: int = 1000, chunk_overlap: int = 200
) -> Generator[str, None, None]:
    """
    01-04: 处理整个目录下的文档
    优化点：
    1. 使用多进程并行处理
    2. 使用生成器减少内存使用
    3. 优化文件扩展名检查

    Args:
        directory_path (str): 目录路径
        chunk_size (int): 每个块的大小
        chunk_overlap (int): 块之间的重叠大小

    Yields:
        str: 文本块
    """
    if not os.path.isdir(directory_path):
        raise NotADirectoryError(f"目录不存在: {directory_path}")

    # 优化文件扩展名检查
    supported_extensions = (".txt", ".pdf", ".docx")
    files = [
        f
        for f in os.listdir(directory_path)
        if any(f.lower().endswith(ext) for ext in supported_extensions)
    ]

    # 使用多进程处理文件
    with Pool() as pool:
        # 使用偏函数固定参数
        process_func = partial(
            process_single_file, chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

        # 并行处理文件
        for chunks in tqdm(
            pool.imap(process_func, [os.path.join(directory_path, f) for f in files]),
            total=len(files),
            desc="处理文档",
        ):
            # 使用生成器逐个返回文本块
            for chunk in chunks:
                yield chunk


# 测试代码
if __name__ == "__main__":
    # 测试文档加载
    test_file = "./07-Rag/data/test.txt"
    try:
        # 测试单个文件处理
        text = load_document(test_file)
        print(f"文档加载成功，长度: {len(text)}")

        # 测试文本预处理
        processed_text = preprocess_text(text)
        print(f"预处理后长度: {len(processed_text)}")

        # 测试文本分块
        chunks = split_text(processed_text)
        print(f"分块数量: {len(chunks)}")
        print("所有分块的内容:")
        for i, chunk in enumerate(chunks):
            print(f"块 {i+1}: {chunk[:100]}...")

        # 测试目录处理
        print("\n测试目录处理:")
        for i, chunk in enumerate(process_directory("./07-Rag/data")):
            print(f"目录块 {i+1}: {chunk[:100]}...")

    except Exception as e:
        print(f"测试失败: {str(e)}")
