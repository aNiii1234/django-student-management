#!/usr/bin/env python
"""
团队共享数据库设置脚本
用于初始化团队共享的用户数据系统
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

from django.core.management import execute_from_command_line
from django.contrib.auth import get_user_model
from accounts.models import User

def setup_team_database():
    """
    设置团队共享数据库
    """
    print("=" * 60)
    print("Django 学生管理系统 - 团队数据库设置")
    print("=" * 60)

    # 1. 运行数据库迁移
    print("\n1. 正在运行数据库迁移...")
    try:
        execute_from_command_line(['manage.py', 'migrate'])
        print("✓ 数据库迁移完成")
    except Exception as e:
        print(f"✗ 数据库迁移失败: {e}")
        return False

    # 2. 创建管理员用户
    print("\n2. 创建管理员用户...")
    try:
        User = get_user_model()

        # 检查是否已存在管理员
        if User.objects.filter(role='admin').exists():
            print("✓ 已存在管理员用户")
            admins = User.objects.filter(role='admin')
            for admin in admins:
                print(f"  - {admin.username} ({admin.get_role_display()})")
        else:
            # 创建默认管理员
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@team.com',
                password='admin123',
                role='admin',
                first_name='管理员',
                last_name='系统'
            )
            print(f"✓ 创建默认管理员用户: {admin_user.username}")
            print("  用户名: admin")
            print("  密码: admin123")
            print("  角色: 管理员")

    except Exception as e:
        print(f"✗ 创建管理员失败: {e}")
        return False

    # 3. 创建示例教师用户
    print("\n3. 创建示例教师用户...")
    try:
        if not User.objects.filter(role='teacher').exists():
            teacher = User.objects.create_user(
                username='teacher',
                email='teacher@team.com',
                password='teacher123',
                role='teacher',
                first_name='张',
                last_name='老师',
                phone='13800138000'
            )
            print(f"✓ 创建示例教师用户: {teacher.username}")
            print("  用户名: teacher")
            print("  密码: teacher123")
            print("  角色: 教师")
        else:
            print("✓ 已存在教师用户")

    except Exception as e:
        print(f"✗ 创建教师用户失败: {e}")

    # 4. 创建示例学生用户
    print("\n4. 创建示例学生用户...")
    try:
        if not User.objects.filter(role='student').exists():
            student = User.objects.create_user(
                username='student',
                email='student@team.com',
                password='student123',
                role='student',
                first_name='李',
                last_name='同学',
                phone='13800138001'
            )
            print(f"✓ 创建示例学生用户: {student.username}")
            print("  用户名: student")
            print("  密码: student123")
            print("  角色: 学生")
        else:
            print("✓ 已存在学生用户")

    except Exception as e:
        print(f"✗ 创建学生用户失败: {e}")

    # 5. 显示当前用户统计
    print("\n5. 当前用户统计:")
    try:
        User = get_user_model()
        admin_count = User.objects.filter(role='admin').count()
        teacher_count = User.objects.filter(role='teacher').count()
        student_count = User.objects.filter(role='student').count()

        print(f"  管理员: {admin_count} 人")
        print(f"  教师: {teacher_count} 人")
        print(f"  学生: {student_count} 人")
        print(f"  总计: {admin_count + teacher_count + student_count} 人")

    except Exception as e:
        print(f"✗ 统计用户失败: {e}")

    # 6. 显示团队访问信息
    print("\n6. 团队访问配置:")
    print("✓ 团队数据库设置完成！")
    print("\n团队成员访问方法:")
    print("1. 确保能访问项目文件夹")
    print("2. 运行: python manage.py runserver 0.0.0.0:8000")
    print("3. 其他成员通过浏览器访问: http://[你的IP地址]:8000")
    print("\n默认测试账号:")
    print("- 管理员: admin / admin123")
    print("- 教师: teacher / teacher123")
    print("- 学生: student / student123")

    return True

def create_team_members():
    """
    批量创建团队成员账号
    """
    print("\n7. 批量创建团队成员账号:")

    team_members = [
        # 教师账号
        {'username': 'wang_teacher', 'password': 'wang123', 'role': 'teacher', 'first_name': '王', 'last_name': '老师'},
        {'username': 'li_teacher', 'password': 'li123', 'role': 'teacher', 'first_name': '李', 'last_name': '老师'},

        # 学生账号
        {'username': 'zhang_student', 'password': 'zhang123', 'role': 'student', 'first_name': '张', 'last_name': '三'},
        {'username': 'li_student', 'password': 'li123', 'role': 'student', 'first_name': '李', 'last_name': '四'},
        {'username': 'wang_student', 'password': 'wang123', 'role': 'student', 'first_name': '王', 'last_name': '五'},
    ]

    User = get_user_model()
    created_count = 0

    for member_data in team_members:
        try:
            if not User.objects.filter(username=member_data['username']).exists():
                user = User.objects.create_user(
                    username=member_data['username'],
                    email=f"{member_data['username']}@team.com",
                    password=member_data['password'],
                    role=member_data['role'],
                    first_name=member_data['first_name'],
                    last_name=member_data['last_name']
                )
                print(f"✓ 创建 {member_data['role']} 用户: {member_data['username']} / {member_data['password']}")
                created_count += 1
            else:
                print(f"- 用户 {member_data['username']} 已存在")
        except Exception as e:
            print(f"✗ 创建用户 {member_data['username']} 失败: {e}")

    print(f"\n成功创建 {created_count} 个团队成员账号")

if __name__ == '__main__':
    success = setup_team_database()

    if success:
        # 询问是否创建更多团队成员
        try:
            response = input("\n是否创建更多示例团队成员账号？(y/n): ").lower().strip()
            if response in ['y', 'yes', '是']:
                create_team_members()
        except:
            pass  # 在非交互环境中跳过

    print("\n" + "=" * 60)
    print("团队数据库设置完成！")
    print("=" * 60)