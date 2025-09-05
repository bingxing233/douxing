#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import time

def main():
    # 检查是否已创建虚拟环境
    venv_path = os.path.join(os.path.dirname(__file__), '.venv')
    if not os.path.exists(venv_path):
        print("创建Python虚拟环境...")
        subprocess.run([sys.executable, '-m', 'venv', '.venv'], cwd=os.path.dirname(__file__))
    
    # 激活虚拟环境并安装依赖
    print("安装依赖...")
    if os.name == 'nt':  # Windows
        pip_path = os.path.join(venv_path, 'Scripts', 'pip')
    else:  # Unix/Linux/macOS
        pip_path = os.path.join(venv_path, 'bin', 'pip')
    
    subprocess.run([pip_path, 'install', '-r', 'requirements.txt'], cwd=os.path.dirname(__file__))
    
    # 启动后端服务
    print("启动后端服务...")
    if os.name == 'nt':  # Windows
        python_path = os.path.join(venv_path, 'Scripts', 'python')
    else:  # Unix/Linux/macOS
        python_path = os.path.join(venv_path, 'bin', 'python')
    
    subprocess.Popen([python_path, 'main.py'], cwd=os.path.dirname(__file__))
    print("后端服务已启动，访问地址: http://localhost:8000")

if __name__ == "__main__":
    main()