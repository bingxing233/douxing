# backend/agents/job_analyzer.py
from nat.agent.tool_calling_agent.agent import ToolCallAgentGraph as Agent
from nat.llm.openai_llm import OpenAIModelConfig
import os
import yaml
import json
import re

class JobAnalyzerAgent(Agent):
    def __init__(self):
        # 从环境变量获取API密钥
        qwen_api_key = os.getenv("QWEN_API_KEY")
        
        # 检查API密钥是否存在
        if not qwen_api_key:
            raise ValueError("QWEN_API_KEY环境变量未设置，请检查.env文件配置")
        
        # 初始化LLM
        llm = OpenAIModelConfig(
            model="qwen2-72b-instruct",
            api_key=qwen_api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )
        
        # 调用父类构造函数
        super().__init__(
            llm=llm,
            tools=[],  # 岗位分析暂时不需要工具
            system_prompt=self._get_system_prompt()
        )
    
    def _get_system_prompt(self):
        """获取系统提示"""
        return """
        你是一个专业的职位分析专家，能够准确解析职位描述中的关键信息。
        请从职位描述中提取以下信息：
        1. 职位名称
        2. 公司名称
        3. 工作地点
        4. 薪资范围
        5. 工作经验要求
        6. 学历要求
        7. 技能要求（关键技术栈）
        8. 工作职责
        9. 任职要求
        10. 公司福利
        11. 工作类型（全职/兼职/实习）
        12. 行业领域
        
        请以结构化的格式输出结果。
        """
    
    def parse_job_description(self, job_description: str) -> dict:
        """分析职位描述并提取关键信息"""
        prompt = f"""
        请分析以下职位描述并以标准JSON格式输出结果：
        
        职位描述：
        {job_description}
        
        请严格按照以下格式输出，且必须返回有效的JSON格式：
        {{
            "position": "职位名称",
            "company": "公司名称",
            "location": "工作地点",
            "salary_range": "薪资范围",
            "experience_required": "工作经验要求",
            "education_required": "学历要求",
            "skills": ["技能1", "技能2", "技能3"],
            "responsibilities": ["职责1", "职责2"],
            "requirements": ["要求1", "要求2"],
            "benefits": ["福利1", "福利2"],
            "employment_type": "工作类型",
            "industry": "行业领域"
        }}
        
        重要：只返回JSON，不要包含其他文字或解释。
        """
        
        try:
            # 使用run方法运行Agent
            response = self.run(prompt)
            
            # 这里应该解析响应并返回结构化数据
            # 为简化，我们直接返回响应
            return {"raw_response": response}
        except Exception as e:
            return {"error": f"分析职位描述时出错: {str(e)}"}
    
    