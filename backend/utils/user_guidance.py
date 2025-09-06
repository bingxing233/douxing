// backend/utils/user_guidance.py
from typing import Dict, List
import os

class UserGuidance:
    """用户引导和帮助系统"""
    
    def __init__(self):
        self.guides = self._load_guides()
    
    def _load_guides(self) -> Dict[str, str]:
        """加载用户引导内容"""
        return {
            "welcome": """
欢迎使用中小微企业智能招聘助手！
本系统可以帮助您自动化完成招聘流程，包括：
1. 岗位需求理解 - 将模糊的岗位描述转换为标准化职位描述
2. 简历自动筛选 - 自动解析简历并与岗位需求匹配
3. 初轮沟通自动化 - 通过AI进行初步候选人沟通
4. 面试邀约同步 - 自动生成面试邀请并同步日程

点击左侧菜单开始使用各项功能。
            """,
            
            "job_analysis": """
岗位需求理解功能使用说明：
1. 在输入框中描述您要招聘的岗位（可以是模糊描述）
2. 点击"生成标准化岗位需求"按钮
3. 系统将自动生成详细的岗位描述，包括：
   - 岗位名称
   - 核心职责
   - 任职要求（学历、经验、技能等）
            """,
            
            "resume_screening": """
简历筛选功能使用说明：
1. 首先输入岗位ID（可通过岗位需求理解功能获取）
2. 上传候选人的简历文件（支持PDF、DOCX、TXT格式）
3. 点击"开始筛选"按钮
4. 系统将自动分析简历与岗位的匹配度，并给出评分
            """,
            
            "common_issues": """
常见问题及解决方案：

Q: 上传简历后提示格式错误怎么办？
A: 请确保简历文件为PDF、DOCX或TXT格式，文件大小不超过10MB。

Q: 系统生成的岗位描述不准确怎么办？
A: 请尽量详细地描述岗位需求，包括技能要求、经验年限、学历要求等。

Q: 简历筛选结果不理想怎么办？
A: 可以调整岗位描述中的关键词，或者在筛选后手动调整匹配度评分。

Q: 如何自定义初轮沟通话术？
A: 管理员可以在系统配置中添加自定义沟通模板。
            """
        }
    
    def get_guide(self, guide_name: str) -> str:
        """获取指定引导内容"""
        return self.guides.get(guide_name, "未找到相关引导内容")
    
    def get_all_guides(self) -> Dict[str, str]:
        """获取所有引导内容"""
        return self.guides
    
    def get_quick_start_guide(self) -> str:
        """获取快速开始引导"""
        return """
快速开始指南：
1. 首先使用"岗位需求理解"功能生成标准化职位描述
2. 然后使用"简历筛选"功能筛选候选人简历
3. 对于匹配度高的候选人，可以使用"初轮沟通"功能进行初步沟通
4. 最后使用"面试邀约"功能安排面试时间
        """
    
    def get_system_status(self) -> Dict[str, str]:
        """获取系统状态信息"""
        return {
            "backend_status": "运行中",
            "frontend_status": "运行中",
            "ai_model_status": "已连接",
            "last_updated": "2023-01-01 12:00:00"
        }
    
    def get_troubleshooting_tips(self, error_code: str = None) -> List[str]:
        """获取故障排除建议"""
        tips = [
            "检查网络连接是否正常",
            "确认API密钥是否正确配置",
            "查看系统日志了解详细错误信息",
            "重启服务尝试解决问题"
        ]
        
        if error_code == "FILE_UPLOAD_ERROR":
            tips.extend([
                "检查文件格式是否为PDF、DOCX或TXT",
                "确认文件大小不超过10MB",
                "尝试重新上传文件"
            ])
        elif error_code == "AI_MODEL_ERROR":
            tips.extend([
                "检查API密钥是否有效",
                "确认模型服务是否正常运行",
                "查看是否达到API调用限制"
            ])
        
        return tips

class ErrorHandler:
    """错误处理和用户提示"""
    
    @staticmethod
    def format_error_for_user(error: Exception) -> str:
        """将错误格式化为用户友好的提示"""
        error_msg = str(error)
        
        # 根据错误类型提供具体建议
        if "Python" in error_msg and "version" in error_msg:
            return "Python版本不兼容，请升级到Python 3.8或更高版本"
        elif "ModuleNotFoundError" in error_msg:
            return "缺少必要的依赖包，请运行'pip install -r requirements.txt'安装依赖"
        elif "ConnectionError" in error_msg:
            return "网络连接失败，请检查网络设置和API服务状态"
        elif "PermissionError" in error_msg:
            return "权限不足，请以管理员身份运行程序或检查文件权限"
        else:
            return f"操作失败：{error_msg}"
    
    @staticmethod
    def log_error(error: Exception, context: str = ""):
        """记录错误日志"""
        import logging
        logging.error(f"错误上下文: {context}, 错误信息: {error}", exc_info=True)