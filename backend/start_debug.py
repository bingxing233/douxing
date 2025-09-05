#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import traceback

def main():
    try:
        print("开始启动后端服务...")
        print("当前工作目录:", os.getcwd())
        
        # 检查配置文件
        config_path = os.path.join("..", "configs", "recruitment_config.yml")
        if os.path.exists(config_path):
            print("✓ 配置文件存在")
        else:
            print("✗ 配置文件不存在:", config_path)
            
        # 检查环境变量文件
        env_path = os.path.join("..", ".env")
        if os.path.exists(env_path):
            print("✓ 环境变量文件存在")
        else:
            print("⚠ 环境变量文件不存在:", env_path)
            
        # 尝试导入必要的模块
        try:
            import fastapi
            print("✓ FastAPI模块可用")
        except ImportError as e:
            print("✗ FastAPI模块不可用:", str(e))
            
        try:
            import uvicorn
            print("✓ Uvicorn模块可用")
        except ImportError as e:
            print("✗ Uvicorn模块不可用:", str(e))
            
        try:
            import yaml
            print("✓ PyYAML模块可用")
        except ImportError as e:
            print("✗ PyYAML模块不可用:", str(e))
            
        # 尝试导入主应用
        try:
            sys.path.append(os.path.dirname(__file__))
            from main import app
            print("✓ 主应用导入成功")
        except Exception as e:
            print("✗ 主应用导入失败:", str(e))
            traceback.print_exc()
            
        # 启动服务
        print("尝试启动服务...")
        from main import app
        import uvicorn
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
        
    except Exception as e:
        print("启动过程中发生错误:", str(e))
        traceback.print_exc()

if __name__ == "__main__":
    main()