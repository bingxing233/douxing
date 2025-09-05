// backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.job_parser import router as job_router
from api.resume_screener import router as resume_router
from dotenv import load_dotenv
import os
import yaml

# 加载环境变量
load_dotenv()

app = FastAPI(title="招聘辅助Agent API")

# 从环境变量获取配置
SERVICE_PORT = int(os.getenv("SERVICE_PORT", "8000"))
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"

# 从配置文件加载模型配置
try:
    with open("configs/recruitment_config.yml", "r") as f:
        config = yaml.safe_load(f)
    app.state.model_config = config["models"]["qwen"]
except Exception as e:
    print(f"警告: 无法加载配置文件: {e}")
    app.state.model_config = {
        "model_name": "qwen-plus",
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "temperature": 0.7,
        "max_tokens": 2048
    }

# 跨域配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境需限制来源
    allow_methods=["*"],
    allow_headers=["*"]
)

# 注册路由
app.include_router(job_router, prefix="/api")
app.include_router(resume_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=SERVICE_PORT, reload=DEBUG_MODE)