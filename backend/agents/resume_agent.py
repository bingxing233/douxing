// backend/agents/resume_agent.py
from nemo_agent import Agent, Toolkit
from nemo_agent.llms import OpenAICompatible
import os
import yaml

class ResumeScreenerAgent(Agent):
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
    
    def screen_resumes(self, resume_texts, job_requirements):
        """根据岗位需求筛选简历"""
        results = []
        for text in resume_texts:
            # 简化：实际需提取简历关键信息
            score = self._calculate_match_score(text, job_requirements)
            results.append({
                "match_score": score,
                "match_level": "匹配" if score >=70 else "待评估" if score >=40 else "不匹配",
                "reason": self._generate_reason(text, job_requirements, score)
            })
        return results
    
    def _calculate_match_score(self, resume_text, requirements):
        """计算匹配分数（简化版）"""
        skills = requirements["requirements"]["skills"]
        match_count = sum(skill.lower() in resume_text.lower() for skill in skills)
        return min(100, int((match_count / len(skills)) * 70 + 30))  # 基础分30+技能匹配分
    
    def _generate_reason(self, resume_text, requirements, score):
        """生成匹配理由"""
        return f"技能匹配度{score}%，经验要求基本符合"