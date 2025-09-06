@echo off
chcp 65001 >nul
title 中小微企业智能招聘助手

echo 中小微企业智能招聘助手启动脚本
echo ================================

REM 检查Node.js是否安装
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Node.js，请先安装Node.js
    pause
    exit /b 1
) else (
    for /f "tokens=*" %%i in ('node --version') do set NODE_VERSION=%%i
    echo 找到 Node.js %NODE_VERSION%
)

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Python，请先安装Python
    pause
    exit /b 1
) else (
    for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
    echo 找到 %PYTHON_VERSION%
)

echo.
echo 1. 启动后端服务...
cd /d "%~dp0backend"

REM 创建并激活虚拟环境
if not exist .venv (
    echo 创建Python虚拟环境...
    python -m venv .venv
)

echo 安装后端依赖...
call .venv\Scripts\activate.bat
pip install -r requirements.txt >nul 2>&1

REM 启动后端服务
echo 启动后端服务...
start "后端服务" /D "%cd%" cmd /c "call .venv\Scripts\activate.bat && python main.py"
cd /d "%~dp0"

REM 等待后端服务启动
echo 等待后端服务启动...
timeout /t 5 /nobreak >nul

echo.
echo 2. 启动前端服务...
cd /d "%~dp0frontend"

echo 安装前端依赖...
npm install >nul 2>&1

echo 启动前端服务...
start "前端服务" /D "%cd%" cmd /c "npm run dev"
cd /d "%~dp0"

echo.
echo 服务启动完成！
echo ===============
echo 前端界面: http://localhost:3000
echo 后端API: http://localhost:8000/api
echo 后端文档: http://localhost:8000/docs
echo.
echo 关闭此窗口不会停止服务
echo 如需停止服务，请运行 stop_project.bat
echo.
pause