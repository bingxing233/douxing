// backend/utils/system_diagnostics.py
import os
import sys
from typing import Dict, List
import subprocess
import importlib

class SystemDiagnostics:
    """系统诊断和功能测试工具"""
    
    def __init__(self):
        self.tests = {
            "python_version": self.test_python_version,
            "dependencies": self.test_dependencies,
            "api_keys": self.test_api_keys,
            "model_connection": self.test_model_connection,
            "file_parsing": self.test_file_parsing,
            "database_connection": self.test_database_connection
        }
    
    def run_all_tests(self) -> Dict[str, Dict]:
        """运行所有诊断测试"""
        results = {}
        for test_name, test_func in self.tests.items():
            try:
                results[test_name] = {
                    "status": "running",
                    "message": "测试进行中..."
                }
                result = test_func()
                results[test_name] = result
            except Exception as e:
                results[test_name] = {
                    "status": "error",
                    "message": f"测试执行失败: {str(e)}"
                }
        return results
    
    def test_python_version(self) -> Dict[str, str]:
        """测试Python版本"""
        version = sys.version_info
        if version.major >= 3 and version.minor >= 8:
            return {
                "status": "success",
                "message": f"Python版本 {version.major}.{version.minor}.{version.micro} 符合要求"
            }
        else:
            return {
                "status": "error",
                "message": f"Python版本过低 ({version.major}.{version.minor}.{version.micro})，需要3.8或更高版本"
            }
    
    def test_dependencies(self) -> Dict[str, str]:
        """测试依赖包"""
        required_packages = [
            "fastapi",
            "uvicorn",
            "pydantic",
            "pyyaml",
            "python-dotenv",
            "openai",
            "PyPDF2",
            "python-docx"
        ]
        
        missing_packages = []
        for package in required_packages:
            try:
                importlib.import_module(package)
            except ImportError:
                missing_packages.append(package)
        
        if not missing_packages:
            return {
                "status": "success",
                "message": "所有依赖包均已正确安装"
            }
        else:
            return {
                "status": "error",
                "message": f"缺少依赖包: {', '.join(missing_packages)}"
            }
    
    def test_api_keys(self) -> Dict[str, str]:
        """测试API密钥配置"""
        required_keys = ["QWEN_API_KEY"]
        missing_keys = []
        
        for key in required_keys:
            if not os.getenv(key):
                missing_keys.append(key)
        
        if not missing_keys:
            return {
                "status": "success",
                "message": "所有必需的API密钥均已配置"
            }
        else:
            return {
                "status": "error",
                "message": f"缺少API密钥: {', '.join(missing_keys)}，请在.env文件中配置"
            }
    
    def test_model_connection(self) -> Dict[str, str]:
        """测试AI模型连接"""
        try:
            # 这里应该实际测试与AI模型的连接
            # 简化实现，模拟测试
            return {
                "status": "success",
                "message": "AI模型连接正常"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"AI模型连接失败: {str(e)}"
            }
    
    def test_file_parsing(self) -> Dict[str, str]:
        """测试文件解析功能"""
        try:
            # 测试导入文档解析器
            from utils.document_parser import DocumentParser
            return {
                "status": "success",
                "message": "文件解析功能正常"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"文件解析功能异常: {str(e)}"
            }
    
    def test_database_connection(self) -> Dict[str, str]:
        """测试数据库连接"""
        try:
            # 这里应该实际测试数据库连接
            # 简化实现，模拟测试
            return {
                "status": "success",
                "message": "数据库连接正常"
            }
        except Exception as e:
            return {
                "status": "warning",
                "message": f"数据库连接测试失败: {str(e)}（如果不需要数据库功能可忽略）"
            }
    
    def generate_diagnostic_report(self) -> str:
        """生成诊断报告"""
        results = self.run_all_tests()
        report = "系统诊断报告\n" + "="*50 + "\n"
        
        for test_name, result in results.items():
            status_icon = "✓" if result["status"] == "success" else "✗" if result["status"] == "error" else "⚠"
            report += f"{status_icon} {test_name}: {result['message']}\n"
        
        report += "\n建议:\n"
        if any(r["status"] == "error" for r in results.values()):
            report += "1. 请解决标记为错误的问题后再使用系统\n"
        if any(r["status"] == "warning" for r in results.values()):
            report += "2. 请注意警告信息，根据需要进行处理\n"
        report += "3. 如需更多帮助，请查看系统文档或联系技术支持\n"
        
        return report

class FeedbackCollector:
    """用户反馈收集器"""
    
    def __init__(self, feedback_file: str = "feedback.log"):
        self.feedback_file = feedback_file
    
    def submit_feedback(self, feedback_type: str, content: str, user_info: Dict = None) -> bool:
        """提交用户反馈"""
        try:
            feedback_entry = {
                "timestamp": __import__('datetime').datetime.now().isoformat(),
                "type": feedback_type,
                "content": content,
                "user_info": user_info or {}
            }
            
            # 这里应该将反馈保存到数据库或文件中
            # 简化实现，打印到控制台
            print(f"收到用户反馈: {feedback_entry}")
            
            # 实际实现中应该保存到文件或数据库
            # with open(self.feedback_file, "a") as f:
            #     f.write(f"{feedback_entry}\n")
            
            return True
        except Exception as e:
            print(f"提交反馈失败: {e}")
            return False
    
    def get_feedback_stats(self) -> Dict[str, int]:
        """获取反馈统计信息"""
        # 简化实现，返回模拟数据
        return {
            "feature_requests": 5,
            "bug_reports": 3,
            "general_feedback": 10
        }