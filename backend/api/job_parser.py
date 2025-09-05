// backend/api/job_parser.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from agents.job_analyzer import JobAnalyzerAgent

router = APIRouter()
agent = JobAnalyzerAgent()

class JobDescriptionRequest(BaseModel):
    description: str

@router.post("/parse-job")
async def parse_job(request: JobDescriptionRequest):
    try:
        result = agent.parse_job_description(request.description)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))