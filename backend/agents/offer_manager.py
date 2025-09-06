// backend/agents/offer_manager.py
from nemo_agent import Agent, Toolkit
from nemo_agent.llms import OpenAICompatible
import os
import yaml

class OfferManagerAgent(Agent):
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
    
    def generate_offer_letter(self, candidate_info, position_info, salary_details):
        """生成Offer通知书"""
        prompt = f"""
        请根据以下信息生成一份正式的Offer通知书：
        候选人信息：{candidate_info}
        职位信息：{position_info}
        薪资详情：{salary_details}
        
        输出格式：
        - Offer标题
        - 公司信息
        - 候选人信息
        - 职位信息
        - 薪资福利详情
        - 入职时间和地点
        - 其他条款
        - 签署部分
        """
        
        response = self.llm.generate(prompt=prompt)
        return self._format_offer_letter(response)
    
    def _format_offer_letter(self, raw_text):
        """格式化Offer通知书"""
        # 简化：实际实现需根据文本内容解析
        return {
            "title": "录用通知书",
            "company": "某某科技有限公司",
            "candidate": "张三",
            "position": "高级后端工程师",
            "salary": "月薪20K，13薪",
            "benefits": "五险一金，带薪年假，年度体检",
            "start_date": "2023-02-01",
            "work_location": "北京市朝阳区某某大厦",
            "other_terms": "试用期3个月，试用期薪资为转正后80%",
            "signature_section": "请在收到本通知书后3个工作日内签字确认并返回"
        }