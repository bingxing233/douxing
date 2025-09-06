# backend/agents/interview_scheduler.py
from nat.agent.tool_calling_agent.agent import ToolCallAgentGraph as Agent
from nat.llm import OpenAICompatible
import os
import yaml
import requests
from typing import Dict, Any
import json

class InterviewSchedulerAgent(Agent):
    def __init__(self):
        # 从环境变量获取API密钥
        qwen_api_key = os.getenv("QWEN_API_KEY")
        
        # 从配置文件加载模型配置
        with open("configs/recruitment_config.yml", "r") as f:
            config = yaml.safe_load(f)
        
        qwen_config = config["models"]["qwen"]
        
        # 初始化LLM（使用阿里云百炼平台Qwen模型）
        llm = OpenAICompatible(
            model=qwen_config["model_name"],
            base_url=qwen_config["base_url"],
            api_key=qwen_api_key,
            temperature=qwen_config["temperature"],
            max_tokens=qwen_config["max_tokens"]
        )
        
        # 调用父类构造函数
        super().__init__(
            llm=llm,
            tools=[],  # 工具将在后续添加
            name="InterviewSchedulerAgent",
            description="安排和同步面试的智能体",
            system_prompt=self._get_system_prompt()
        )
        
        # 加载日程工具配置
        self.calendar_configs = config.get("calendar_integrations", {})
    
    def _get_system_prompt(self):
        """获取系统提示"""
        return """
        你是一个专业的面试安排专家，能够根据候选人信息、职位信息和面试要求生成详细的面试安排。
        请提供具体的时间选项、地点/方式、面试官信息、面试流程和注意事项。
        """
    
    def schedule_interview(self, candidate_info, job_info, interview_info):
        """安排面试"""
        prompt = f"""
        请根据以下信息生成面试安排：
        候选人信息：{candidate_info}
        职位信息：{job_info}
        面试信息：{interview_info}
        
        输出格式要求：
        请严格按照以下JSON格式输出，不要包含其他文字：
        {{
            "time_options": [
                {{
                    "datetime": "2023-01-10T10:00:00",
                    "timezone": "Asia/Shanghai",
                    "format": "yyyy-MM-dd HH:mm"
                }},
                {{
                    "datetime": "2023-01-10T14:00:00",
                    "timezone": "Asia/Shanghai",
                    "format": "yyyy-MM-dd HH:mm"
                }}
            ],
            "location": "面试地点或在线会议链接",
            "interviewer": ["面试官姓名1", "面试官姓名2"],
            "process": "面试流程描述",
            "notes": "注意事项",
            "duration": 60
        }}
        """
        
        try:
            response = self.run(prompt)
            interview_details = self._format_interview_details(response)
            
            # 同步到日程工具
            sync_results = self._sync_to_calendars(interview_details)
            
            return {
                "status": "success",
                "data": interview_details,
                "sync_results": sync_results
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"安排面试时出错: {str(e)}",
                "error_detail": str(e)
            }
    
    def _format_interview_details(self, raw_response):
        """格式化面试详情"""
        try:
            # 尝试解析JSON
            if isinstance(raw_response, str):
                # 清理和解析JSON
                start = raw_response.find('{')
                end = raw_response.rfind('}')
                if start != -1 and end != -1:
                    json_str = raw_response[start:end+1]
                    details = json.loads(json_str)
                    return details
            elif isinstance(raw_response, dict):
                return raw_response
        except Exception as e:
            print(f"解析面试详情时出错: {e}")
        
        # 返回默认格式
        return {
            "time_options": [
                {
                    "datetime": "2023-01-10T10:00:00",
                    "timezone": "Asia/Shanghai",
                    "format": "yyyy-MM-dd HH:mm"
                }
            ],
            "location": "待定",
            "interviewer": ["待定"],
            "process": "待定",
            "notes": "无",
            "duration": 60
        }
    
    def _sync_to_calendars(self, interview_details: Dict[str, Any]) -> Dict[str, Any]:
        """同步面试安排到各种日程工具"""
        results = {}
        
        for calendar_name, config in self.calendar_configs.items():
            if not config.get("enabled", False):
                results[calendar_name] = {
                    "status": "skipped",
                    "message": "集成未启用"
                }
                continue
                
            try:
                if calendar_name == "dingtalk":
                    result = self._sync_to_dingtalk(interview_details, config)
                elif calendar_name == "wechat_work":
                    result = self._sync_to_wechat_work(interview_details, config)
                elif calendar_name == "outlook":
                    result = self._sync_to_outlook(interview_details, config)
                elif calendar_name == "google_calendar":
                    result = self._sync_to_google_calendar(interview_details, config)
                else:
                    result = {
                        "status": "error",
                        "message": "不支持的日历系统"
                    }
                    
                results[calendar_name] = result
            except Exception as e:
                results[calendar_name] = {
                    "status": "error",
                    "message": f"同步失败: {str(e)}",
                    "error_detail": str(e)
                }
        
        return results
    
    def _sync_to_dingtalk(self, interview_details: Dict[str, Any], config: Dict[str, str]) -> Dict[str, Any]:
        """同步到钉钉日程"""
        try:
            # 模拟钉钉API调用
            # 实际实现应该调用钉钉的API接口
            # 示例: requests.post(dingtalk_api_url, headers=headers, json=data)
            
            # 检查必需的配置
            if not config.get("app_key") or not config.get("app_secret"):
                return {
                    "status": "error",
                    "message": "缺少钉钉配置: app_key 或 app_secret"
                }
            
            # 构造日程数据
            schedule_data = {
                "title": f"面试: {interview_details.get('position', '未知职位')}",
                "description": f"候选人面试安排\n\n{interview_details.get('process', '')}",
                "location": interview_details.get('location', ''),
                "start_time": interview_details["time_options"][0]["datetime"] if interview_details.get("time_options") else "",
                "end_time": self._calculate_end_time(
                    interview_details["time_options"][0]["datetime"], 
                    interview_details.get("duration", 60)
                ) if interview_details.get("time_options") else "",
                "attendees": interview_details.get("interviewer", [])
            }
            
            # 这里应该是实际的API调用
            # response = requests.post(
            #     "https://oapi.dingtalk.com/topapi/calendar/create",
            #     headers={"Authorization": f"Bearer {access_token}"},
            #     json=schedule_data
            # )
            
            return {
                "status": "success",
                "message": "已模拟同步到钉钉日程",
                "data": schedule_data
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"同步到钉钉失败: {str(e)}",
                "error_detail": str(e)
            }
    
    def _sync_to_wechat_work(self, interview_details: Dict[str, Any], config: Dict[str, str]) -> Dict[str, Any]:
        """同步到企业微信日程"""
        try:
            # 检查必需的配置
            if not config.get("corp_id") or not config.get("secret"):
                return {
                    "status": "error",
                    "message": "缺少企业微信配置: corp_id 或 secret"
                }
            
            # 构造日程数据
            schedule_data = {
                "summary": f"面试: {interview_details.get('position', '未知职位')}",
                "description": f"候选人面试安排\n\n{interview_details.get('process', '')}",
                "location": interview_details.get('location', ''),
                "start_time": interview_details["time_options"][0]["datetime"] if interview_details.get("time_options") else "",
                "end_time": self._calculate_end_time(
                    interview_details["time_options"][0]["datetime"], 
                    interview_details.get("duration", 60)
                ) if interview_details.get("time_options") else "",
                "attendees": interview_details.get("interviewer", [])
            }
            
            # 这里应该是实际的API调用
            # response = requests.post(
            #     "https://qyapi.weixin.qq.com/cgi-bin/calendar/add",
            #     params={"access_token": access_token},
            #     json=schedule_data
            # )
            
            return {
                "status": "success",
                "message": "已模拟同步到企业微信日程",
                "data": schedule_data
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"同步到企业微信失败: {str(e)}",
                "error_detail": str(e)
            }
    
    def _calculate_end_time(self, start_time: str, duration: int) -> str:
        """根据开始时间和持续时间计算结束时间"""
        # 简化实现，实际应该使用日期时间库进行计算
        return start_time  # 在实际实现中应计算正确的结束时间
    
    def _sync_to_outlook(self, interview_details: Dict[str, Any], config: Dict[str, str]) -> Dict[str, Any]:
        """同步到Outlook日程"""
        try:
            # 检查必需的配置
            if not config.get("client_id") or not config.get("client_secret"):
                return {
                    "status": "error",
                    "message": "缺少Outlook配置: client_id 或 client_secret"
                }
            
            # 构造日程数据
            schedule_data = {
                "subject": f"面试: {interview_details.get('position', '未知职位')}",
                "body": {
                    "contentType": "HTML",
                    "content": f"<p>候选人面试安排</p><p>{interview_details.get('process', '')}</p>"
                },
                "location": {
                    "displayName": interview_details.get('location', '')
                },
                "start": {
                    "dateTime": interview_details["time_options"][0]["datetime"] if interview_details.get("time_options") else "",
                    "timeZone": "China Standard Time"
                },
                "end": {
                    "dateTime": self._calculate_end_time(
                        interview_details["time_options"][0]["datetime"], 
                        interview_details.get("duration", 60)
                    ) if interview_details.get("time_options") else "",
                    "timeZone": "China Standard Time"
                },
                "attendees": [
                    {
                        "emailAddress": {
                            "address": interviewer.get("email", "") if isinstance(interviewer, dict) else "",
                            "name": interviewer if isinstance(interviewer, str) else interviewer.get("name", "")
                        },
                        "type": "required"
                    } for interviewer in interview_details.get("interviewer", [])
                ]
            }
            
            # 这里应该是实际的Microsoft Graph API调用
            # response = requests.post(
            #     "https://graph.microsoft.com/v1.0/me/events",
            #     headers={"Authorization": f"Bearer {access_token}"},
            #     json=schedule_data
            # )
            
            return {
                "status": "success",
                "message": "已模拟同步到Outlook日程",
                "data": schedule_data
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"同步到Outlook失败: {str(e)}",
                "error_detail": str(e)
            }
    
    def _sync_to_google_calendar(self, interview_details: Dict[str, Any], config: Dict[str, str]) -> Dict[str, Any]:
        """同步到Google Calendar"""
        try:
            # 检查必需的配置
            if not config.get("client_id") or not config.get("client_secret"):
                return {
                    "status": "error",
                    "message": "缺少Google Calendar配置: client_id 或 client_secret"
                }
            
            # 构造日程数据
            schedule_data = {
                "summary": f"面试: {interview_details.get('position', '未知职位')}",
                "description": f"候选人面试安排\n\n{interview_details.get('process', '')}",
                "location": interview_details.get('location', ''),
                "start": {
                    "dateTime": interview_details["time_options"][0]["datetime"] if interview_details.get("time_options") else "",
                    "timeZone": "Asia/Shanghai"
                },
                "end": {
                    "dateTime": self._calculate_end_time(
                        interview_details["time_options"][0]["datetime"], 
                        interview_details.get("duration", 60)
                    ) if interview_details.get("time_options") else "",
                    "timeZone": "Asia/Shanghai"
                },
                "attendees": [
                    {"email": interviewer.get("email", "")} if isinstance(interviewer, dict) 
                    else {"email": ""} for interviewer in interview_details.get("interviewer", [])
                ]
            }
            
            # 这里应该是实际的Google Calendar API调用
            # service.events().insert(calendarId='primary', body=schedule_data).execute()
            
            return {
                "status": "success",
                "message": "已模拟同步到Google Calendar",
                "data": schedule_data
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"同步到Google Calendar失败: {str(e)}",
                "error_detail": str(e)
            }