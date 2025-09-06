# backend/api/resume_screener.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from agents.resume_agent import ResumeScreenerAgent
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# 初始化Agent
try:
    agent = ResumeScreenerAgent()
    logger.info("ResumeScreenerAgent 初始化成功")
except Exception as e:
    logger.error(f"ResumeScreenerAgent 初始化失败: {str(e)}")
    agent = None

class ResumeScreenRequest(BaseModel):
    resumes: list[str]
    job_requirements: dict

class ResumeScreenResponse(BaseModel):
    status: str
    data: list = None
    message: str = None

@router.post("/screen-resumes", response_model=ResumeScreenResponse)
async def screen_resumes(request: ResumeScreenRequest):
    # 检查Agent是否初始化成功
    if agent is None:
        logger.error("ResumeScreenerAgent 未初始化")
        return ResumeScreenResponse(
            status="error",
            message="服务初始化失败，请检查配置和API密钥"
        )
    
    try:
        logger.info("开始筛选简历")
        results = agent.screen_resumes(request.resumes, request.job_requirements)
        logger.info("简历筛选完成")
        return ResumeScreenResponse(
            status="success",
            data=results
        )
    except Exception as e:
        logger.error(f"筛选简历时出错: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))