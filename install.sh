#!/bin/bash

# 中小微企业智能招聘助手安装脚本

echo "🚀 开始安装中小微企业智能招聘助手..."

# 检查系统要求
echo "🔍 检查系统要求..."

# 检查是否安装了Node.js
if ! command -v node &> /dev/null
then
    echo "❌ 未找到Node.js，请先安装Node.js (版本18+)"
    exit 1
else
    NODE_VERSION=$(node -v)
    echo "✅ Node.js 已安装 ($NODE_VERSION)"
fi

# 检查是否安装了Python
if ! command -v python3 &> /dev/null
then
    echo "❌ 未找到Python3，请先安装Python3 (版本3.8+)"
    exit 1
else
    PYTHON_VERSION=$(python3 -V)
    echo "✅ Python 已安装 ($PYTHON_VERSION)"
fi

# 检查是否安装了Git
if ! command -v git &> /dev/null
then
    echo "❌ 未找到Git，请先安装Git"
    exit 1
else
    GIT_VERSION=$(git --version)
    echo "✅ Git 已安装 ($GIT_VERSION)"
fi

# 安装前端依赖
echo "🌐 安装前端依赖..."
cd frontend
npm install
if [ $? -eq 0 ]; then
    echo "✅ 前端依赖安装完成"
else
    echo "❌ 前端依赖安装失败"
    exit 1
fi
cd ..

# 安装后端依赖
echo "🔧 安装后端依赖..."
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
if [ $? -eq 0 ]; then
    echo "✅ 后端依赖安装完成"
else
    echo "❌ 后端依赖安装失败"
    exit 1
fi
cd ..

# 配置环境变量
if [ ! -f ".env" ]; then
    echo "📝 配置环境变量..."
    cp .env.example .env
    echo "✅ 环境变量文件已创建，请编辑 .env 文件填入实际的API密钥"
else
    echo "✅ 环境变量文件已存在"
fi

echo ""
echo "🎉 安装完成！"
echo ""
echo "下一步："
echo "1. 请编辑 .env 文件，填入实际的API密钥"
echo "2. 运行 ./start.sh 启动服务"
echo "3. 访问 http://localhost:3000 使用应用"