// backend/agents/candidate_tracker.py
from nemo_agent import Agent, Toolkit
from nemo_agent.llms import OpenAICompatible
import os
import yaml

class CandidateTrackerAgent(Agent):
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
    
    def update_candidate_status(self, candidate_id, status, notes=""):
        """更新候选人状态"""
        # 简化：实际应与数据库交互
        return {
            "candidate_id": candidate_id,
            "status": status,
            "timestamp": "2023-01-01T00:00:00Z",
            "notes": notes
        }
    
    def generate_followup_plan(self, candidate_info, current_status):
        """生成候选人跟进计划"""
        prompt = f"""
        请根据以下候选人信息和当前状态，生成下一步跟进计划：
        候选人信息：{candidate_info}
        当前状态：{current_status}
        
        输出格式：
        - 下一步行动建议
        - 预计时间安排
        - 负责人建议
        - 注意事项
        """
        
        response = self.llm.generate(prompt=prompt)
        return self._format_followup_plan(response)
    
    def _format_followup_plan(self, raw_text):
        """格式化跟进计划"""
        # 简化：实际实现需根据文本内容解析
        return {
            "next_action": "发送offer并确认入职时间",
            "schedule": "2023-01-05T00:00:00Z",
            "responsible_person": "HR经理",
            "notes": "候选人已通过所有面试环节"
        }