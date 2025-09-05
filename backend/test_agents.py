// backend/test_agents.py
import unittest
import os
import yaml
from agents.job_analyzer import JobAnalyzerAgent
from agents.resume_agent import ResumeScreenerAgent

class TestAgents(unittest.TestCase):
    def setUp(self):
        # 设置环境变量
        os.environ['QWEN_API_KEY'] = 'test_api_key'
        
        # 加载配置
        with open("configs/recruitment_config.yml", "r") as f:
            self.config = yaml.safe_load(f)
        
    def test_job_analyzer(self):
        """测试岗位解析智能体基本功能"""
        agent = JobAnalyzerAgent()
        self.assertIsNotNone(agent)
        
        # 测试岗位解析功能
        result = agent.parse_job_description("招会做Excel的行政")
        self.assertIsInstance(result, dict)
        self.assertIn("title", result)
        self.assertIn("responsibilities", result)
        self.assertIn("requirements", result)
        
        # 验证返回结果结构
        self.assertIsInstance(result["title"], str)
        self.assertIsInstance(result["responsibilities"], str)
        self.assertIsInstance(result["requirements"], dict)
        
    def test_resume_screener(self):
        """测试简历筛选智能体基本功能"""
        agent = ResumeScreenerAgent()
        self.assertIsNotNone(agent)
        
        # 测试简历筛选功能
        job_requirements = {
            "title": "行政专员",
            "requirements": {
                "education": "大专及以上",
                "experience": "1年以上行政经验",
                "skills": ["Excel", "沟通协调", "文档编写"]
            }
        }
        
        # 测试单个简历筛选
        result = agent.screen_resumes([
            "具备2年行政经验，精通Excel和Word，有良好的沟通能力"
        ], job_requirements)
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertIn("match_score", result[0])
        self.assertIn("match_level", result[0])
        self.assertIn("reason", result[0])
        
        # 验证匹配分数范围
        self.assertGreaterEqual(result[0]["match_score"], 0)
        self.assertLessEqual(result[0]["match_score"], 100)

if __name__ == '__main__':
    unittest.main()