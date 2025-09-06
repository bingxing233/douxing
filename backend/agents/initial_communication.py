// backend/agents/initial_communication.py
from nemo_agent import Agent, Toolkit
from nemo_agent.llms import OpenAICompatible
import os
import yaml

class InitialCommunicationAgent(Agent):
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
        
        # 加载自定义沟通话术配置
        self.communication_templates = config.get("communication_templates", {})
    
    def conduct_initial_communication(self, candidate_info, job_requirements, template_name="default"):
        """进行初轮沟通"""
        # 获取沟通模板
        template = self.communication_templates.get(template_name, self._get_default_template())
        
        prompt = f"""
        你是一个专业的HR招聘人员，请根据以下信息与候选人进行初轮沟通：
        
        候选人信息：
        {candidate_info}
        
        职位要求：
        {job_requirements}
        
        沟通模板：
        {template}
        
        请生成一段自然、专业的沟通对话，包括：
        1. 问候和自我介绍
        2. 确认候选人求职意向
        3. 介绍职位基本信息
        4. 询问关键信息（如薪资期望、到岗时间等）
        5. 安排下一步流程
        """
        
        response = self.llm.generate(prompt=prompt)
        return self._format_communication_result(response)
    
    def _get_default_template(self):
        """获取默认沟通模板"""
        return """
        1. 问候和自我介绍
        2. 确认对方是否为[候选人姓名]
        3. 简要介绍公司和职位
        4. 询问对方目前求职状态
        5. 了解对方薪资期望和到岗时间
        6. 确认对方是否有其他面试或offer
        7. 介绍下一步流程（如正式面试安排）
        """
    
    def _format_communication_result(self, raw_text):
        """格式化沟通结果"""
        # 简化：实际实现需根据文本内容解析
        return {
            "dialogue": raw_text,
            "candidate_response": "候选人反馈信息",
            "key_info_extracted": {
                "salary_expectation": "薪资期望",
                "availability": "到岗时间",
                "other_offers": "其他面试/offer情况"
            },
            "next_steps": "下一步安排建议"
        }
    
    def load_custom_template(self, template_name, template_content):
        """加载自定义沟通模板"""
        self.communication_templates[template_name] = template_content
        return {"status": "success", "message": f"模板 {template_name} 已加载"}