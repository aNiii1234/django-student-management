#!/usr/bin/env python
"""
测试用户管理功能的脚本
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management.settings')
django.setup()

from accounts.models import User
from django.test import TestCase
from django.contrib.auth import get_user_model

def test_user_visibility():
    print("=== 用户可见性测试 ===")

    # 1. 检查所有用户
    all_users = User.objects.all()
    print(f"数据库总用户数: {all_users.count()}")

    # 2. 检查各角色用户
    admin_users = User.objects.filter(role='admin')
    student_users = User.objects.filter(role='student')
    teacher_users = User.objects.filter(role='teacher')

    print(f"管理员用户数: {admin_users.count()}")
    print(f"学生用户数: {student_users.count()}")
    print(f"教师用户数: {teacher_users.count()}")

    # 3. 详细显示所有用户信息
    print("\n=== 详细用户信息 ===")
    for user in all_users:
        print(f"ID: {user.id}")
        print(f"用户名: {user.username}")
        print(f"邮箱: {user.email}")
        print(f"角色: {user.role} ({user.get_role_display()})")
        print(f"姓名: {user.get_full_name()}")
        print(f"手机号: {user.phone}")
        print(f"是否激活: {user.is_active}")
        print(f"是否员工: {user.is_staff}")
        print(f"是否超级用户: {user.is_superuser}")
        print(f"创建时间: {user.created_at}")
        print("-" * 50)

def test_admin_can_see_all_users():
    print("\n=== 管理员权限测试 ===")

    # 获取管理员用户
    admin_user = User.objects.filter(role='admin').first()
    if not admin_user:
        print("❌ 没有找到管理员用户")
        return

    print(f"管理员用户: {admin_user.username}")

    # 模拟管理员查看所有用户的查询
    all_users_for_admin = User.objects.all()
    students_for_admin = User.objects.filter(role='student')

    print(f"管理员可以看到所有用户: {all_users_for_admin.count()} 个")
    print(f"管理员可以看到学生用户: {students_for_admin.count()} 个")

    # 显示学生用户列表（管理员视角）
    print("\n管理员视角下的学生用户:")
    for student in students_for_admin:
        print(f"- {student.username} ({student.email}) - 注册时间: {student.created_at}")

def test_recent_users():
    print("\n=== 最近注册用户测试 ===")

    from django.utils import timezone
    from datetime import timedelta

    # 最近3天注册的用户
    three_days_ago = timezone.now() - timedelta(days=3)
    recent_users = User.objects.filter(created_at__gte=three_days_ago)

    print(f"最近3天注册的用户数: {recent_users.count()}")

    for user in recent_users:
        print(f"- {user.username} ({user.get_role_display()}) - {user.created_at}")

def main():
    try:
        test_user_visibility()
        test_admin_can_see_all_users()
        test_recent_users()
        print("\n✅ 所有测试完成")
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()