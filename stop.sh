#!/bin/bash

# 停止中小微企业智能招聘助手服务

echo "🛑 停止中小微企业智能招聘助手服务..."

# 查找并终止前端进程
FRONTEND_PIDS=$(ps aux | grep "next dev" | grep -v grep | awk '{print $2}')
if [ ! -z "$FRONTEND_PIDS" ]; then
    echo "📱 停止前端服务 (PID: $FRONTEND_PIDS)"
    kill $FRONTEND_PIDS
else
    echo "📱 前端服务未运行"
fi

# 查找并终止后端进程
BACKEND_PIDS=$(ps aux | grep "main.py" | grep -v grep | awk '{print $2}')
if [ ! -z "$BACKEND_PIDS" ]; then
    echo "🔧 停止后端服务 (PID: $BACKEND_PIDS)"
    kill $BACKEND_PIDS
else
    echo "🔧 后端服务未运行"
fi

# 清理日志文件
if [ -f "frontend/frontend.log" ]; then
    echo "🗑  清理前端日志文件"
    rm frontend/frontend.log
fi

if [ -f "backend/backend.log" ]; then
    echo "🗑  清理后端日志文件"
    rm backend/backend.log
fi

echo "✅ 服务已停止"