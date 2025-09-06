#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import traceback

def main():
    try:
        print("当前工作目录:", os.getcwd())
        print("Python路径:", sys.executable)
        
        # 添加项目根目录到Python路径
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sys.path.insert(0, project_root)
        print("项目根目录:", project_root)
        
        # 尝试导入必要的模块
        print("正在导入模块...")
        from backend.main import app
        print("模块导入成功")
        
        # 启动服务
        print("正在启动服务...")
        import uvicorn
        uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)
        
    except Exception as e:
        print(f"启动服务时发生错误: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()