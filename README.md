# 中小微企业智能招聘辅助Agent

这是一个基于NVIDIA NeMo Agent Toolkit构建的中小微企业智能招聘助手，用于自动化完成招聘全流程，包括岗位需求理解、简历自动筛选、初轮沟通自动化、面试邀约同步、面试评价记录、候选人跟进、offer发放和入职提醒等功能。

## 项目结构
```
.
├── README.md
├── package.json
├── .gitignore
├── .env.example
├── start.sh                 # Linux/macOS启动脚本
├── stop.sh                  # Linux/macOS停止脚本
├── start.bat                # Windows启动脚本
├── stop.bat                 # Windows停止脚本
├── configs/
│   └── recruitment_config.yml
├── frontend/
│   ├── next.config.js
│   ├── tsconfig.json
│   ├── package.json
│   └── app/
│       ├── job-parser/
│       │   └── page.tsx
│       └── resume-screener/
│           └── page.tsx
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── api/
│   │   ├── job_parser.py
│   │   └── resume_screener.py
│   ├── agents/
│   │   ├── job_analyzer.py
│   │   ├── resume_agent.py
│   │   ├── interview_evaluator.py
│   │   ├── candidate_tracker.py
│   │   ├── offer_manager.py
│   │   ├── initial_communication.py
│   │   └── interview_scheduler.py
│   ├── utils/
│   │   ├── document_parser.py
│   │   ├── data_security.py
│   │   ├── api_key_manager.py
│   │   ├── model_manager.py
│   │   ├── user_guidance.py
│   │   └── system_diagnostics.py
│   └── plugins/
│       └── plugin_manager.py
└── mcp/
    └── simple_protocol.py
```

## 🎯 核心功能

- **岗位需求理解**：将模糊的岗位描述转换为标准化职位描述（JD）
- **简历自动筛选**：自动解析简历并与岗位需求匹配，支持PDF、Word、TXT等多种格式
- **初轮沟通自动化**：通过AI进行初步候选人沟通，支持自定义沟通话术
- **面试邀约同步**：自动生成面试邀请并同步到主流日程工具（钉钉、企业微信、Outlook等）
- **面试评价记录**：自动生成面试评价报告，记录面试官反馈
- **候选人跟进**：自动跟进候选人状态，生成后续行动计划
- **Offer发放**：自动生成Offer通知书，支持模板自定义
- **入职提醒**：自动发送入职提醒和准备事项清单

## 🚀 快速开始

### 系统要求

- Python 3.8+
- Node.js 18+
- Git

### 一键启动（推荐）

#### Linux/macOS

```bash
# 启动服务
./start.sh

# 停止服务
./stop.sh
```

#### Windows

```cmd
# 启动服务
start.bat

# 停止服务
stop.bat
```

## 🔗 前后端衔接说明

本项目采用前后端分离架构：

### 后端 (FastAPI)
- 地址: http://localhost:8000
- API文档: http://localhost:8000/docs
- 提供RESTful API接口供前端调用

### 前端 (Next.js)
- 地址: http://localhost:3000
- 通过axios库调用后端API
- 开发环境下通过Next.js的rewrites功能代理API请求到后端

### API接口
1. 岗位需求解析: POST /api/parse-job
2. 简历筛选: POST /api/screen-resumes

## 开发环境搭建指南

### 前端开发环境搭建
1. 确保已安装Node.js（版本18.0.0或更高）
2. 确保已安装npm（版本8.0.0或更高）
3. 安装项目依赖：
   ```bash
   cd frontend
   npm install
   ```
4. 启动开发服务器：
   ```bash
   npm run dev
   ```
5. 访问 http://localhost:3000 查看前端界面

### 后端开发环境搭建
1. 确保已安装Python 3.8或更高版本
2. 创建并激活虚拟环境：
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   .venv\Scripts\activate   # Windows
   ```
3. 安装项目依赖：
   ```bash
   pip install -r requirements.txt
   ```
4. 启动后端服务：
   ```bash
   python main.py
   ```

## 🌐 访问地址

- 前端界面: http://localhost:3000
- 后端API: http://localhost:8000/api
- API文档: http://localhost:8000/docs

## ⚙️ 项目配置

### API密钥管理

1. **敏感信息保护**：
   - 所有包含敏感信息的文件（如`.env`文件）都应被添加到`.gitignore`文件中，以防止意外提交到版本控制系统中
   - .gitignore文件已包含以下内容：
     ```bash
     # Sensitive information
     .env
     .env.*
     *.key
     *.secret
     ```

2. **配置文件说明**：
   - `configs/recruitment_config.yml`：主配置文件，包含API密钥配置、模型配置和服务配置
   - `.env`：本地环境变量配置文件（不会提交到Git）
   - `.env.example`：环境变量配置示例文件

3. **阿里云百炼平台Qwen模型配置**：
   - 默认使用Qwen模型：qwen-plus
   - API基础URL：https://dashscope.aliyuncs.com/compatible-mode/v1
   - 温度参数：0.7（控制生成文本的随机性）
   - 最大令牌数：2048（控制生成文本的长度）

### 环境变量配置

1. 复制环境变量示例文件：
   ```bash
   cp .env.example .env  # Linux/macOS
   copy .env.example .env  # Windows
   ```

2. 编辑`.env`文件，填入实际的API密钥：
   ```env
   # Qwen API Key for main AI model
   QWEN_API_KEY=your_actual_qwen_api_key_here
   
   # Tavily API Key for internet search
   TAVILY_API_KEY=your_actual_tavily_api_key_here
   
   # NVIDIA API Key
   NVIDIA_API_KEY=your_actual_nvidia_api_key_here
   
   # Encryption key for data security
   ENCRYPTION_KEY=your_secret_encryption_key_here
   ```

## 🔧 系统优化说明

### 1. 全流程招聘支持
项目现已覆盖招聘全流程，包括前期（岗位分析、简历筛选）、中期（初轮沟通、面试安排、面试评价）和后期（候选人跟进、Offer发放、入职提醒）。

### 2. 增强的简历处理能力
- 支持PDF、Word、TXT、Excel等多种格式的简历解析
- 提供可自定义的筛选规则，满足不同企业个性化需求
- 增强的候选人信息提取和结构化处理

### 3. 落地性更强的沟通与邀约功能
- 支持自定义初轮沟通话术模板
- 集成主流日程工具（钉钉、企业微信、Outlook、Google Calendar）
- 实现真正的自动化日程同步

### 4. 安全性增强
- 简历数据加密存储
- API密钥权限管理和自动轮换
- 敏感信息遮蔽和访问控制
- HTTPS传输安全支持

### 5. 插件化架构和可扩展性
- 实现插件化架构，支持功能模块热插拔
- 支持多种AI模型的切换和集成
- 提供统一的扩展接口

### 6. 用户体验优化
- 提供详细的用户引导和帮助文档
- 增强错误提示和故障排除机制
- 内置系统诊断和自检功能
- 提供用户反馈渠道

## 🧪 功能测试

### 岗位需求理解测试

```
用户: 我需要一个Python后端工程师，熟悉FastAPI和数据库设计，有3年以上经验
AI: [生成标准化职位描述]
```

### 简历筛选测试

```
用户: 帮我筛选这份简历，看是否符合Python后端工程师职位要求
AI: [分析简历并给出匹配度评估]
```

## 🛠 技术架构

- **前端**: Next.js 14 + TypeScript
- **后端**: FastAPI + Python
- **AI框架**: NVIDIA NeMo Agent Toolkit
- **大模型**: 阿里云百炼平台Qwen系列模型
- **工作流**: React Agent模式

## 🔒 安全建议

1. 不要将API密钥提交到版本控制系统
2. 在生产环境中使用HTTPS
3. 定期轮换API密钥
4. 限制API密钥的权限范围
5. 定期清理过期简历数据

## 📚 相关资源

- [NVIDIA NeMo Agent Toolkit文档](https://docs.nvidia.com/nemo/)
- [阿里云百炼平台](https://bailian.console.aliyun.com/)
- [Qwen模型文档](https://help.aliyun.com/zh/qwen/)
- [FastAPI文档](https://fastapi.tiangolo.com/)
- [Next.js文档](https://nextjs.org/docs)