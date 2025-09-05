@echo off
chcp 65001 >nul
title 中小微企业智能招聘助手

echo 正在启动中小微企业智能招聘助手...
echo.

echo 启动后端服务...
cd backend

REM 创建并激活虚拟环境
if not exist .venv (
    echo 创建Python虚拟环境...
    python -m venv .venv
)

echo 激活虚拟环境并安装依赖...
call .venv\Scripts\activate.bat
pip install -r requirements.txt

REM 启动后端服务
echo 启动后端服务...
start "后端服务" /D "%cd%" cmd /c "call .venv\Scripts\activate.bat && python main.py"
cd ..

REM 等待后端服务启动
echo 等待后端服务启动...
timeout /t 5 /nobreak >nul

echo 启动前端服务...
cd frontend

echo 安装前端依赖...
npm install

echo 启动前端服务...
start "前端服务" /D "%cd%" cmd /c "npm run dev"
cd ..

echo.
echo 服务启动完成！
echo.
echo 前端界面: http://localhost:3000
echo 后端API: http://localhost:8000/api
echo 后端文档: http://localhost:8000/docs
echo.
echo 关闭此窗口不会停止服务
echo.
pause