@echo off
chcp 65001 >nul
title 停止招聘助手服务

echo 停止中小微企业智能招聘助手服务
echo ================================

echo 正在停止前端服务...
taskkill /f /im node.exe 2>nul

echo 正在停止后端服务...
taskkill /f /im python.exe 2>nul

echo.
echo 服务已停止
echo ==========
echo.
pause