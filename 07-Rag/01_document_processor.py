import os
from typing import List, Union
import re
from docx import Document
from PyPDF2 import PdfReader
from tqdm import tqdm

def load_document(file_path: str) -> str:
    """
    01-01: 加载文档内容
    支持的文件格式：txt, pdf, docx
    
    Args:
        file_path (str): 文档路径
        
    Returns:
        str: 文档内容
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    file_ext = os.path.splitext(file_path)[1].lower()
    
    if file_ext == '.txt':
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    elif file_ext == '.pdf':
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    elif file_ext == '.docx':
        doc = Document(file_path)
        return '\n'.join([paragraph.text for paragraph in doc.paragraphs])
    else:
        raise ValueError(f"不支持的文件格式: {file_ext}")

def preprocess_text(text: str) -> str:
    """
    01-02: 文本预处理
    1. 移除多余空白字符
    2. 标准化换行符
    3. 移除特殊字符
    
    Args:
        text (str): 原始文本
        
    Returns:
        str: 处理后的文本
    """
    # 移除多余空白字符
    text = re.sub(r'\s+', ' ', text)
    # 标准化换行符
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    # 移除特殊字符
    text = re.sub(r'[^\w\s\u4e00-\u9fff]', '', text)
    return text.strip()

def split_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[str]:
    """
    01-03: 将文本分割成块
    使用滑动窗口方法进行分块，保持语义完整性
    
    Args:
        text (str): 待分割的文本
        chunk_size (int): 每个块的大小
        chunk_overlap (int): 块之间的重叠大小
        
    Returns:
        List[str]: 文本块列表
    """
    if not text:
        return []
    
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = min(start + chunk_size, text_length)
        
        # 如果还没到文本末尾，尝试在句子边界处分割
        if end < text_length:
            # 查找最近的句子结束符
            sentence_end = max(
                text.rfind('.', start, end),
                text.rfind('。', start, end),
                text.rfind('!', start, end),
                text.rfind('！', start, end),
                text.rfind('?', start, end),
                text.rfind('？', start, end),
                text.rfind('\n', start, end)
            )
            
            if sentence_end > start:
                end = sentence_end + 1
        
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        start = end - chunk_overlap
    
    return chunks

def process_directory(directory_path: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[str]:
    """
    01-04: 处理整个目录下的文档
    
    Args:
        directory_path (str): 目录路径
        chunk_size (int): 每个块的大小
        chunk_overlap (int): 块之间的重叠大小
        
    Returns:
        List[str]: 所有文档的文本块列表
    """
    if not os.path.isdir(directory_path):
        raise NotADirectoryError(f"目录不存在: {directory_path}")
    
    all_chunks = []
    supported_extensions = {'.txt', '.pdf', '.docx'}
    
    # 获取所有支持的文件
    files = [f for f in os.listdir(directory_path) 
             if os.path.splitext(f)[1].lower() in supported_extensions]
    
    for file in tqdm(files, desc="处理文档"):
        file_path = os.path.join(directory_path, file)
        try:
            # 加载文档
            text = load_document(file_path)
            # 预处理
            text = preprocess_text(text)
            # 分块
            chunks = split_text(text, chunk_size, chunk_overlap)
            all_chunks.extend(chunks)
        except Exception as e:
            print(f"处理文件 {file} 时出错: {str(e)}")
    
    return all_chunks

# 测试代码
if __name__ == "__main__":
    # 测试文档加载
    test_file = "./07-Rag/data/test.txt"
    try:
        text = load_document(test_file)
        print(f"文档加载成功，长度: {len(text)}")
        
        # 测试文本预处理
        processed_text = preprocess_text(text)
        print(f"预处理后长度: {len(processed_text)}")
        
        # 测试文本分块
        chunks = split_text(processed_text)
        print(f"分块数量: {len(chunks)}")
        print("前两个块的内容:")
        for i, chunk in enumerate(chunks[:2]):
            print(f"块 {i+1}: {chunk[:100]}...")
            
    except Exception as e:
        print(f"测试失败: {str(e)}") 