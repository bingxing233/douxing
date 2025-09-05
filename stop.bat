@echo off
title 停止招聘助手服务

echo 🛑 停止中小微企业智能招聘助手服务...

REM 查找并终止前端服务进程
echo 📱 停止前端服务...
taskkill /f /im node.exe 2>nul

REM 查找并终止后端服务进程
echo 🔧 停止后端服务...
taskkill /f /im python.exe 2>nul

echo.
echo ✅ 服务已停止
echo.
pause