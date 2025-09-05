// backend/api/resume_screener.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from agents.resume_agent import ResumeScreenerAgent

router = APIRouter()
agent = ResumeScreenerAgent()

class ResumeScreeningRequest(BaseModel):
    resume_texts: list[str]
    job_requirements: dict

@router.post("/screen-resumes")
async def screen_resumes(request: ResumeScreeningRequest):
    try:
        results = agent.screen_resumes(request.resume_texts, request.job_requirements)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))