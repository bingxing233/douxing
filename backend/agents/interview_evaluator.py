// backend/agents/interview_evaluator.py
from nemo_agent import Agent, Toolkit
from nemo_agent.llms import OpenAICompatible
import os
import yaml

class InterviewEvaluatorAgent(Agent):
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
    
    def evaluate_candidate(self, candidate_info, interview_notes):
        """评估候选人并生成评价报告"""
        prompt = f"""
        请根据以下候选人信息和面试记录，生成面试评价报告：
        候选人信息：{candidate_info}
        面试记录：{interview_notes}
        
        输出格式：
        - 综合评分（满分100分）
        - 优势分析
        - 待改进点
        - 是否推荐进入下一轮面试（是/否）
        - 推荐岗位匹配度分析
        """
        
        response = self.llm.generate(prompt=prompt)
        return self._format_evaluation(response)
    
    def _format_evaluation(self, raw_text):
        """格式化评价结果"""
        # 简化：实际实现需根据文本内容解析
        return {
            "score": 85,
            "strengths": "技术能力强，沟通能力好",
            "improvements": "缺乏大型项目管理经验",
            "recommend_next_round": True,
            "position_match_analysis": "与岗位要求匹配度较高"
        }