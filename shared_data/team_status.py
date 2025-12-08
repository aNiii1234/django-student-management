#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
团队系统状态检查脚本
"""

import os
import sys
import django
from pathlib import Path

# 添加项目路径到Python路径
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root / 'student_management'))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management.settings')

try:
    django.setup()
except Exception as e:
    print(f"Django设置失败: {e}")
    sys.exit(1)

from django.contrib.auth import get_user_model
from accounts.models import User
from students.models import StudentProfile
from django.conf import settings

def check_team_status():
    """
    检查团队系统状态
    """
    print("=" * 50)
    print("Django 学生管理系统 - 团队状态检查")
    print("=" * 50)

    # 1. 数据库配置检查
    print("\n1. 数据库配置:")
    db_path = settings.DATABASES['default']['NAME']
    print(f"   数据库路径: {db_path}")
    print(f"   数据库存在: {'是' if db_path.exists() else '否'}")
    if db_path.exists():
        size_mb = db_path.stat().st_size / (1024 * 1024)
        print(f"   文件大小: {size_mb:.2f} MB")

    # 2. 用户统计
    print("\n2. 用户统计:")
    User = get_user_model()
    total_users = User.objects.count()
    admin_count = User.objects.filter(role='admin').count()
    teacher_count = User.objects.filter(role='teacher').count()
    student_count = User.objects.filter(role='student').count()

    print(f"   总用户数: {total_users}")
    print(f"   管理员: {admin_count}")
    print(f"   教师: {teacher_count}")
    print(f"   学生: {student_count}")

    # 3. 学生档案统计
    print("\n3. 学生档案:")
    total_profiles = StudentProfile.objects.count()
    print(f"   学生档案数: {total_profiles}")

    # 4. 最近的用户活动
    print("\n4. 最近创建的用户:")
    recent_users = User.objects.order_by('-created_at')[:5]
    for user in recent_users:
        print(f"   {user.username} ({user.get_role_display()}) - {user.created_at.strftime('%Y-%m-%d %H:%M')}")

    # 5. 团队访问信息
    print("\n5. 团队访问配置:")
    print(f"   DEBUG模式: {'开启' if settings.DEBUG else '关闭'}")
    print(f"   允许的主机: {', '.join(settings.ALLOWED_HOSTS)}")
    print(f"   会话存储: {settings.SESSION_ENGINE}")

    # 6. 测试账号
    print("\n6. 测试账号:")
    test_accounts = [
        ("管理员", "admin", "admin123"),
        ("教师", "teacher", "teacher123"),
        ("学生", "student", "student123"),
    ]
    for role, username, password in test_accounts:
        print(f"   {role}: {username} / {password}")

    # 7. 状态总结
    print("\n7. 系统状态:")
    status = "正常" if total_users >= 3 else "需要配置"
    print(f"   整体状态: {status}")

    if db_path.exists() and total_users >= 3:
        print("   ✓ 团队共享系统已就绪")
    else:
        print("   ✗ 需要进一步配置")

    return total_users >= 3

if __name__ == '__main__':
    is_ready = check_team_status()

    print("\n" + "=" * 50)
    if is_ready:
        print("团队系统已就绪，可以开始使用！")
    else:
        print("请先完成系统配置。")
    print("=" * 50)