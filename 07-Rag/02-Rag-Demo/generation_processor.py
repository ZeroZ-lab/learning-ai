import dashscope
from dotenv import load_dotenv
import os
from datetime import datetime
from typing import List, Tuple

load_dotenv()
dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")


class GenerationProcessor:
    def __init__(self, model_name: str = "qwen-max"):
        """初始化生成处理器

        Args:
            model_name: 使用的模型名称，默认为 qwen-max
        """
        self.model = model_name
        print("\n=== 初始化生成处理器 ===")
        print(f"模型: {self.model}")
        print("=" * 50)

    def generate_response(
        self, query: str, reranked_results: List[Tuple[str, float]], top_k: int = 3
    ) -> str:
        """使用大模型生成回答

        Args:
            query: 用户查询
            reranked_results: 重排序后的结果列表，每个元素为(内容, 分数)
            top_k: 使用前k个结果作为上下文

        Returns:
            str: 生成的回答
        """
        print("\n=== 开始生成回答 ===")
        print(f"查询: {query}")
        print(f"使用前 {top_k} 个相关结果作为上下文")
        print("-" * 50)

        try:
            # 构建提示词
            context = "\n".join(
                [
                    f"参考内容 {i+1}: {result[0]}"
                    for i, result in enumerate(reranked_results[:top_k])
                ]
            )
            prompt = f"""基于以下参考内容，请回答用户的问题。如果参考内容中没有相关信息，请说明无法回答。

参考内容：
{context}

用户问题：{query}

请用中文回答："""

            start_time = datetime.now()
            response = dashscope.Generation.call(
                model=self.model,
                prompt=prompt,
                temperature=0.7,
                top_p=0.8,
                result_format="message",
                stream=False,
                incremental_output=False,
            )
            duration = (datetime.now() - start_time).total_seconds()

            if response.status_code == 200:
                result = response.output.choices[0].message.content
                print(f"生成完成，耗时: {duration:.2f}秒")
                print("=" * 50)
                return result
            else:
                error_msg = f"生成失败: {response.message}"
                print(error_msg)
                print("=" * 50)
                return error_msg

        except Exception as e:
            error_msg = f"生成出错: {str(e)}"
            print(error_msg)
            print("=" * 50)
            return error_msg
