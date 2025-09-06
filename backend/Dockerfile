# 使用官方Python运行时作为基础镜像，升级到3.11版本以满足NeMo-Agent-Toolkit的要求
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制requirements.txt并安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 安装git（用于可能的依赖安装）
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# 复制应用代码
COPY . .

# 安装mcp依赖和NeMo-Agent-Toolkit
RUN pip install --no-cache-dir mcp~=1.13
RUN pip install --no-cache-dir git+https://github.com/NVIDIA/NeMo-Agent-Toolkit.git

# 安装langgraph依赖（指定兼容版本）
RUN pip install --no-cache-dir "langgraph~=0.2.50"

# 设置PYTHONPATH
ENV PYTHONPATH=/app

# 暴露端口
EXPOSE 8000

# 启动应用
CMD ["python", "main.py"]