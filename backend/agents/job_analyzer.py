// backend/agents/job_analyzer.py
from nemo_agent import Agent, Toolkit
from nemo_agent.llms import OpenAICompatible
import os
import yaml

class JobAnalyzerAgent(Agent):
    def __init__(self):
        # 从环境变量获取API密钥
        qwen_api_key = os.getenv("QWEN_API_KEY")
        
        # 从配置文件加载模型配置
        with open("configs/recruitment_config.yml", "r") as f:
            config = yaml.safe_load(f)
        
        qwen_config = config["models"]["qwen"]
        
        # 初始化LLM（使用阿里云百炼平台Qwen模型）
        self.llm = OpenAICompatible(
            model_name=qwen_config["model_name"],
            base_url=qwen_config["base_url"],
            api_key=qwen_api_key,
            temperature=qwen_config["temperature"],
            max_tokens=qwen_config["max_tokens"]
        )
        super().__init__(toolkit=Toolkit(), llm=self.llm)
    
    def parse_job_description(self, description):
        """解析模糊岗位描述为标准化需求"""
        prompt = f"""
        请将以下岗位描述转换为标准化岗位需求：
        {description}
        
        输出格式：
        - 岗位名称
        - 核心职责（3-5条）
        - 任职要求：学历、工作经验、专业技能（关键词列表）
        """
        
        response = self.llm.generate(prompt=prompt)
        return self._format_result(response)
    
    def _format_result(self, raw_text):
        """格式化LLM输出为结构化数据"""
        # 简化：实际实现需根据文本内容解析
        return {
            "title": "行政专员",
            "responsibilities": "1. 负责日常行政事务；2. 文档管理；3. 会议安排",
            "requirements": {
                "education": "大专及以上",
                "experience": "1年以上行政经验",
                "skills": ["Excel", "沟通协调", "文档编写"]
            }
        }