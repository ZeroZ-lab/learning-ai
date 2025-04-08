# Learning AI

## TLDR;

这是一个 AI 学习项目，包含从基础到高级的多个实践模块：
- 🤖 LLM 基础对话
- 🔄 函数调用
- 🖼️ 多模态应用
- 🌐 Web 应用开发
- 📚 RAG 系统实现

快速开始：
```bash
git clone <repo> && cd learning-ai
python -m venv .venv && source .venv/bin/activate
uv pip install -e .
```

这是一个用于学习和实践 AI 应用开发的项目，包含多个模块来展示不同的 AI 功能和应用场景。

## 项目结构

```
.
├── 01-HelloLLM/         # LLM基础入门示例
├── 02-Advanced-Chat/    # 高级对话功能示例
├── 03-Function-Calling/ # 函数调用功能示例
├── 04-Multi-Modal/      # 多模态应用示例
├── 05-app/             # Web应用示例
├── 06-app-server/      # 后端服务示例
└── 07-Rag/             # 检索增强生成(RAG)示例
```

## 环境要求

- Python >= 3.12
- 推荐使用 uv 包管理器

## 快速开始

1. **克隆项目**
```bash
git clone <repository-url>
cd learning-ai
```

2. **环境配置**
```bash
# 创建并激活虚拟环境
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate    # Windows

# 安装依赖
uv pip install -e .
```

3. **配置环境变量**
```bash
cp .env.example .env
# 编辑 .env 文件，填入必要的 API 密钥
```

## 主要依赖

- openai >= 1.70.0：OpenAI API 客户端
- faiss-cpu >= 1.10.0：向量检索库
- pandas >= 2.2.3：数据处理
- tqdm >= 4.67.1：进度条显示
- 其他文件处理库：openpyxl, pypdf2, python-docx

## 模块说明

### 01-HelloLLM
LLM 基础应用示例，包含基本的对话和文本生成功能。

### 02-Advanced-Chat
展示高级对话功能，包含上下文管理和对话控制。

### 03-Function-Calling
演示如何使用 LLM 的函数调用能力。

### 04-Multi-Modal
多模态应用示例，展示图像和文本的结合应用。

### 05-app
Web 应用示例，展示如何构建 AI 驱动的 Web 应用。

### 06-app-server
后端服务示例，提供 AI 功能的 API 接口。

### 07-Rag
检索增强生成(RAG)示例，展示如何结合文档检索和 LLM 生成。

## 使用说明

每个模块都包含独立的示例和说明文档，请参考各模块下的 README 文件获取详细使用说明。

## 注意事项

1. 请确保在使用前正确配置环境变量
2. 建议使用虚拟环境运行项目
3. 部分功能需要相应的 API 密钥

## 贡献指南

欢迎提交 Issue 和 Pull Request 来帮助改进项目。

## Roadmap 🗺️

未来计划添加的主要功能：

- [ ] 本地模型部署完整指南

_注：Roadmap 会根据技术发展和社区需求持续更新_

## 许可证

[MIT License](LICENSE)
