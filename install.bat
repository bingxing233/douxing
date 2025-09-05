@echo off
title 中小微企业智能招聘助手安装程序

echo 🚀 开始安装中小微企业智能招聘助手...
echo.

REM 检查系统要求
echo 🔍 检查系统要求...

REM 检查Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未找到Node.js，请先安装Node.js (版本18+)
    pause
    exit /b 1
) else (
    for /f "tokens=*" %%i in ('node --version') do set NODE_VERSION=%%i
    echo ✅ Node.js 已安装 (%NODE_VERSION%)
)

REM 检查Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未找到Python，请先安装Python (版本3.8+)
    pause
    exit /b 1
) else (
    for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
    echo ✅ Python 已安装 (%PYTHON_VERSION%)
)

REM 检查Git
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未找到Git，请先安装Git
    pause
    exit /b 1
) else (
    for /f "tokens=*" %%i in ('git --version') do set GIT_VERSION=%%i
    echo ✅ Git 已安装 (%GIT_VERSION%)
)

REM 安装前端依赖
echo.
echo 🌐 安装前端依赖...
cd frontend
npm install
if %errorlevel% equ 0 (
    echo ✅ 前端依赖安装完成
) else (
    echo ❌ 前端依赖安装失败
    cd ..
    pause
    exit /b 1
)
cd ..

REM 安装后端依赖
echo.
echo 🔧 安装后端依赖...
cd backend
if not exist .venv (
    echo 🐍 创建Python虚拟环境...
    python -m venv .venv
)
echo 💿 激活虚拟环境并安装依赖...
call .venv\Scripts\activate.bat
pip install -r requirements.txt
if %errorlevel% equ 0 (
    echo ✅ 后端依赖安装完成
) else (
    echo ❌ 后端依赖安装失败
    cd ..
    pause
    exit /b 1
)
cd ..

REM 配置环境变量
if not exist .env (
    echo.
    echo 📝 配置环境变量...
    copy .env.example .env >nul
    echo ✅ 环境变量文件已创建，请编辑 .env 文件填入实际的API密钥
) else (
    echo.
    echo ✅ 环境变量文件已存在
)

echo.
echo 🎉 安装完成！
echo.
echo 下一步：
echo 1. 请编辑 .env 文件，填入实际的API密钥
echo 2. 运行 start.bat 启动服务
echo 3. 访问 http://localhost:3000 使用应用
echo.
pause