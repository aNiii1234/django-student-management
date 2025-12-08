#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
创建团队用户脚本
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

def create_team_users():
    """
    创建团队用户
    """
    print("=" * 50)
    print("创建团队用户")
    print("=" * 50)

    # 默认用户列表
    default_users = [
        {
            'username': 'admin',
            'password': 'admin123',
            'email': 'admin@team.com',
            'role': 'admin',
            'first_name': '管理员',
            'last_name': '系统',
            'is_superuser': True,
            'is_staff': True
        },
        {
            'username': 'teacher',
            'password': 'teacher123',
            'email': 'teacher@team.com',
            'role': 'teacher',
            'first_name': '张',
            'last_name': '老师',
            'is_superuser': False,
            'is_staff': False
        },
        {
            'username': 'student',
            'password': 'student123',
            'email': 'student@team.com',
            'role': 'student',
            'first_name': '李',
            'last_name': '同学',
            'is_superuser': False,
            'is_staff': False
        }
    ]

    # 额外团队成员
    extra_users = [
        {
            'username': 'wang_teacher',
            'password': 'wang123',
            'email': 'wang_teacher@team.com',
            'role': 'teacher',
            'first_name': '王',
            'last_name': '老师',
            'is_superuser': False,
            'is_staff': False
        },
        {
            'username': 'li_teacher',
            'password': 'li123',
            'email': 'li_teacher@team.com',
            'role': 'teacher',
            'first_name': '李',
            'last_name': '老师',
            'is_superuser': False,
            'is_staff': False
        },
        {
            'username': 'zhang_student',
            'password': 'zhang123',
            'email': 'zhang_student@team.com',
            'role': 'student',
            'first_name': '张',
            'last_name': '三',
            'is_superuser': False,
            'is_staff': False
        },
        {
            'username': 'li_student',
            'password': 'li123',
            'email': 'li_student@team.com',
            'role': 'student',
            'first_name': '李',
            'last_name': '四',
            'is_superuser': False,
            'is_staff': False
        },
        {
            'username': 'wang_student',
            'password': 'wang123',
            'email': 'wang_student@team.com',
            'role': 'student',
            'first_name': '王',
            'last_name': '五',
            'is_superuser': False,
            'is_staff': False
        }
    ]

    all_users = default_users + extra_users
    created_count = 0
    updated_count = 0

    User = get_user_model()

    for user_data in all_users:
        try:
            user, created = User.objects.update_or_create(
                username=user_data['username'],
                defaults=user_data
            )

            if created:
                user.set_password(user_data['password'])
                user.save()
                print(f"创建用户: {user.username} (密码: {user_data['password']})")
                created_count += 1
            else:
                print(f"用户已存在: {user.username}")
                updated_count += 1

        except Exception as e:
            print(f"创建用户失败 {user_data['username']}: {e}")

    # 显示统计信息
    print("\n" + "-" * 30)
    print("用户统计:")
    admin_count = User.objects.filter(role='admin').count()
    teacher_count = User.objects.filter(role='teacher').count()
    student_count = User.objects.filter(role='student').count()

    print(f"管理员: {admin_count} 人")
    print(f"教师: {teacher_count} 人")
    print(f"学生: {student_count} 人")
    print(f"总计: {admin_count + teacher_count + student_count} 人")
    print(f"新创建: {created_count} 人")
    print(f"已存在: {updated_count} 人")

    print("\n测试账号:")
    print("管理员: admin / admin123")
    print("教师: teacher / teacher123")
    print("学生: student / student123")

if __name__ == '__main__':
    create_team_users()