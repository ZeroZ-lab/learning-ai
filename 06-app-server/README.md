# LLM Learning API Server

这是 LLM Learning Path 项目的 API 服务器，基于 FastAPI 构建。

## 功能特点

- RESTful API 设计
- OpenAI 集成
- 自动 API 文档
- CORS 支持
- 环境配置管理

## 快速开始

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 配置环境变量：
复制 `.env.example` 到 `.env` 并填写必要的配置项。

3. 启动服务器：
```bash
uvicorn app.main:app --reload
```

4. 访问 API 文档：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API 端点

- GET /: 欢迎页面
- GET /health: 健康检查
- POST /api/v1/chat: LLM 聊天接口 