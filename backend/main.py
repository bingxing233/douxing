# backend/main.py
import sys
import os

# 将NeMo-Agent-Toolkit添加到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'NeMo-Agent-Toolkit', 'src'))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from api.job_parser import router as job_router
from api.resume_screener import router as resume_router
from dotenv import load_dotenv
import os
import yaml
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

app = FastAPI(title="HR Assistant API", description="中小微企业智能招聘助手API")

# 从环境变量获取配置
SERVICE_PORT = int(os.getenv("SERVICE_PORT", "8000"))
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"

# 从配置文件加载模型配置
try:
    with open("configs/recruitment_config.yml", "r") as f:
        config = yaml.safe_load(f)
    app.state.model_config = config["models"]["qwen"]
    logger.info("配置文件加载成功")
except Exception as e:
    logger.warning(f"警告: 无法加载配置文件: {e}")
    app.state.model_config = {
        "model_name": "qwen-plus",
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "temperature": 0.7,
        "max_tokens": 2048
    }

# 检查必要的环境变量
required_env_vars = ["QWEN_API_KEY"]
missing_env_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_env_vars:
    logger.error(f"缺少必要的环境变量: {', '.join(missing_env_vars)}")
    logger.error("请确保已创建 .env 文件并配置了所有必要的API密钥")

# 跨域配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境需限制来源
    allow_methods=["*"],
    allow_headers=["*"]
)

# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"全局异常处理: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "服务器内部错误", "error_message": str(exc)}
    )

# 包含路由
app.include_router(job_router, prefix="/api/v1/job", tags=["job"])
app.include_router(resume_router, prefix="/api/v1/resume", tags=["resume"])

@app.get("/")
async def root():
    return {"message": "欢迎使用中小微企业智能招聘助手API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    logger.info(f"启动服务: host=0.0.0.0, port={SERVICE_PORT}, debug={DEBUG_MODE}")
    uvicorn.run("main:app", host="0.0.0.0", port=SERVICE_PORT, reload=DEBUG_MODE)