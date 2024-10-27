@echo off
chcp 65001 >nul
title 高清图片转 ICO 工具
cls

echo ================================
echo    欢迎使用高清图片转 ICO 工具
echo ================================
echo.
echo 正在启动程序...

:: 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python，请确保已安装 Python 并添加到系统环境变量。
    pause
    exit
)

:: 检查并安装必要的库
echo 正在检查必要的库...
pip install --upgrade pip

pip install gradio Pillow

:: 设置工作目录
cd /d %~dp0

:: 启动程序
echo 程序启动后将自动打开浏览器...
echo 关闭此窗口即可停止程序运行。
echo.
echo ================================

python Image-to-ico.py

if errorlevel 1 (
    echo.
    echo [错误] 程序运行出现错误，请检查以上信息。
    pause
)
