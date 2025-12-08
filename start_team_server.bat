@echo off
chcp 65001
echo ========================================
echo Django 学生管理系统 - 团队服务器启动
echo ========================================
echo.
echo 正在启动团队共享服务器...
echo.

cd /d "%~dp0student_management"

python manage.py runserver 0.0.0.0:8000

pause