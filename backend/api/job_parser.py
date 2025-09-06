# backend/api/job_parser.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from agents.job_analyzer import JobAnalyzerAgent
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# 初始化Agent时添加错误处理
try:
    agent = JobAnalyzerAgent()
    logger.info("JobAnalyzerAgent 初始化成功")
except Exception as e:
    logger.error(f"JobAnalyzerAgent 初始化失败: {str(e)}")
    agent = None

class JobDescriptionRequest(BaseModel):
    description: str

class JobParseResponse(BaseModel):
    status: str
    data: dict = None
    message: str = None
    error_detail: str = None

@router.post("/parse-job", response_model=JobParseResponse)
async def parse_job(request: JobDescriptionRequest):
    # 检查Agent是否初始化成功
    if agent is None:
        logger.error("JobAnalyzerAgent 未初始化")
        return JobParseResponse(
            status="error",
            message="服务初始化失败，请检查配置和API密钥",
            error_detail="JobAnalyzerAgent 未初始化"
        )
    
    try:
        logger.info("开始解析岗位描述")
        result = agent.parse_job_description(request.description)
        logger.info("岗位描述解析完成")
        return JobParseResponse(**result)
    except Exception as e:
        logger.error(f"解析岗位描述时出错: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))