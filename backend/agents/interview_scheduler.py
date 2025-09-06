// backend/agents/interview_scheduler.py
from nemo_agent import Agent, Toolkit
from nemo_agent.llms import OpenAICompatible
import os
import yaml
import requests
from typing import Dict, Any

class InterviewSchedulerAgent(Agent):
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
        
        # 加载日程工具配置
        self.calendar_configs = config.get("calendar_integrations", {})
    
    def schedule_interview(self, candidate_info, job_info, interview_info):
        """安排面试"""
        prompt = f"""
        请根据以下信息生成面试安排：
        候选人信息：{candidate_info}
        职位信息：{job_info}
        面试信息：{interview_info}
        
        输出格式：
        - 面试时间建议（多个选项）
        - 面试地点/方式
        - 面试官信息
        - 面试流程
        - 注意事项
        """
        
        response = self.llm.generate(prompt=prompt)
        interview_details = self._format_interview_details(response)
        
        # 同步到日程工具
        self._sync_to_calendars(interview_details)
        
        return interview_details
    
    def _format_interview_details(self, raw_text):
        """格式化面试详情"""
        # 简化：实际实现需根据文本内容解析
        return {
            "time_options": ["2023-01-10 10:00", "2023-01-10 14:00", "2023-01-11 10:00"],
            "location": "北京市朝阳区某某大厦101会议室",
            "interviewer": "技术经理李四",
            "process": "技术面试（60分钟）+ HR面试（30分钟）",
            "notes": "请携带身份证、学历证明、前公司离职证明"
        }
    
    def _sync_to_calendars(self, interview_details: Dict[str, Any]):
        """同步面试安排到各种日程工具"""
        for calendar_name, config in self.calendar_configs.items():
            try:
                if calendar_name == "dingtalk":
                    self._sync_to_dingtalk(interview_details, config)
                elif calendar_name == "wechat_work":
                    self._sync_to_wechat_work(interview_details, config)
                elif calendar_name == "outlook":
                    self._sync_to_outlook(interview_details, config)
                elif calendar_name == "google_calendar":
                    self._sync_to_google_calendar(interview_details, config)
            except Exception as e:
                print(f"同步到{calendar_name}失败: {str(e)}")
    
    def _sync_to_dingtalk(self, interview_details: Dict[str, Any], config: Dict[str, str]):
        """同步到钉钉日程"""
        # 这里应该是实际的钉钉API调用
        print(f"模拟同步到钉钉: {interview_details}")
    
    def _sync_to_wechat_work(self, interview_details: Dict[str, Any], config: Dict[str, str]):
        """同步到企业微信日程"""
        # 这里应该是实际的企业微信API调用
        print(f"模拟同步到企业微信: {interview_details}")
    
    def _sync_to_outlook(self, interview_details: Dict[str, Any], config: Dict[str, str]):
        """同步到Outlook日程"""
        # 这里应该是实际的Outlook API调用
        print(f"模拟同步到Outlook: {interview_details}")
    
    def _sync_to_google_calendar(self, interview_details: Dict[str, Any], config: Dict[str, str]):
        """同步到Google Calendar"""
        # 这里应该是实际的Google Calendar API调用
        print(f"模拟同步到Google Calendar: {interview_details}")