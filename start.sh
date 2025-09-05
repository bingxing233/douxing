#!/bin/bash

# 启动中小微企业智能招聘助手

echo "🚀 启动中小微企业智能招聘助手..."

# 检查是否安装了Node.js
if ! command -v node &> /dev/null
then
    echo "❌ 未找到Node.js，请先安装Node.js"
    exit 1
fi

# 检查是否安装了Python
if ! command -v python3 &> /dev/null
then
    echo "❌ 未找到Python3，请先安装Python3"
    exit 1
fi

# 启动后端服务
echo "🔧 启动后端服务..."
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 在后台启动后端服务
nohup python3 main.py > backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# 等待后端服务启动
sleep 5

# 启动前端服务
echo "🌐 启动前端服务..."
cd frontend
npm install
nohup npm run dev > frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

echo "✅ 服务启动完成！"
echo "🖥  前端界面: http://localhost:3000"
echo "📱 后端API: http://localhost:8000"
echo "📝 后端文档: http://localhost:8000/docs"
echo ""
echo "📌 前端PID: $FRONTEND_PID"
echo "📌 后端PID: $BACKEND_PID"
echo ""
echo "💡 使用 stop.sh 脚本停止服务"