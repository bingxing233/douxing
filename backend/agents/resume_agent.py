# backend/agents/resume_agent.py
from nat.agent.tool_calling_agent.agent import ToolCallAgentGraph as Agent
from nat.llm.openai_llm import OpenAIModelConfig as OpenAICompatible
import os
import yaml

class ResumeScreenerAgent(Agent):
    def __init__(self):
        # 从环境变量获取API密钥
        qwen_api_key = os.getenv("QWEN_API_KEY")
        
        # 检查API密钥是否存在
        if not qwen_api_key:
            raise ValueError("QWEN_API_KEY环境变量未设置，请检查.env文件配置")
        
        # 初始化LLM
        llm = OpenAICompatible(
            model="qwen2-72b-instruct",  # 或其他适当的模型
            api_key=qwen_api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )
        
        # 调用父类构造函数
        super().__init__(
            llm=llm,
            tools=[],  # 简历筛选暂时不需要工具
            system_prompt=self._get_system_prompt()
        )
    
    def _get_system_prompt(self):
        """获取系统提示"""
        return """
        你是一个专业的简历筛选专家，能够准确评估候选人与职位的匹配度。
        请根据职位要求分析简历，并提供详细的匹配度分析。
        """
    
    def screen_resume(self, resume_text: str, job_requirements: dict) -> dict:
        """筛选简历并评估与职位的匹配度"""
        prompt = f"""
        请根据以下职位要求分析简历并评估匹配度：
        
        职位要求：
        {yaml.dump(job_requirements, default_flow_style=False)}
        
        简历内容：
        {resume_text}
        
        请提供以下信息，并严格按照JSON格式输出，不要包含其他文字：
        {{
            "match_score": 85,
            "skills_match": {{
                "matched_skills": ["技能1", "技能2"],
                "missing_skills": ["技能3", "技能4"],
                "additional_skills": ["技能5"]
            }},
            "experience_match": "工作经验匹配度分析",
            "education_match": "学历匹配度分析",
            "strengths": ["优势1", "优势2"],
            "weaknesses": ["不足1", "不足2"],
            "recommendations": ["建议1", "建议2"],
            "overall_assessment": "总体评价"
        }}
        """
        
        try:
            response = self.run(prompt)
            # 返回响应
            return {
                "status": "success",
                "raw_response": response
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"筛选简历时出错: {str(e)}"
            }
    

    def screen_resumes(self, resume_texts: list, job_requirements: dict) -> list:
        """批量筛选简历"""
        results = []
        for i, resume_text in enumerate(resume_texts):
            try:
                result = self.screen_resume(resume_text, job_requirements)
                results.append({
                    "resume_index": i,
                    "result": result
                })
            except Exception as e:
                results.append({
                    "resume_index": i,
                    "result": {
                        "status": "error",
                        "message": f"处理简历时出错: {str(e)}"
                    }
                })
        return results