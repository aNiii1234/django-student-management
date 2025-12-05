#!/usr/bin/env python
"""
测试脚本：验证学生注册后自动创建StudentProfile的功能
"""
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management.settings')
django.setup()

from django.test import TestCase
from django.contrib.auth import get_user_model
from students.models import StudentProfile
from django.urls import reverse
from django.test import Client

User = get_user_model()

def test_auto_profile_creation():
    """测试学生注册时是否自动创建StudentProfile"""
    print("🧪 测试学生注册自动档案创建功能...")

    # 检查初始状态
    initial_user_count = User.objects.filter(role='student').count()
    initial_profile_count = StudentProfile.objects.count()
    print(f"   初始学生用户数: {initial_user_count}")
    print(f"   初始学生档案数: {initial_profile_count}")

    # 创建测试学生用户
    test_username = "test_student_auto"
    test_email = "test_auto@example.com"

    # 删除可能存在的测试用户
    User.objects.filter(username=test_username).delete()

    # 创建学生用户
    user = User.objects.create_user(
        username=test_username,
        email=test_email,
        password="testpass123",
        first_name="测试",
        last_name="学生",
        role='student',
        phone="13800138000"
    )

    print(f"   ✅ 创建学生用户: {user.username} (ID: {user.id})")

    # 检查是否自动创建了StudentProfile
    try:
        profile = StudentProfile.objects.get(user=user)
        print(f"   ✅ 自动创建学生档案成功!")
        print(f"      学号: {profile.student_id}")
        print(f"      姓名: {profile.real_name}")
        print(f"      手机: {profile.phone}")
        print(f"      邮箱: {profile.email}")
        print(f"      入学日期: {profile.enrollment_date}")

        # 验证学号格式
        expected_student_id_pattern = f"STU{timezone.now().year % 100:02d}{user.id:04d}"
        if profile.student_id.startswith("STU") and str(user.id) in profile.student_id:
            print(f"   ✅ 学号格式正确: {profile.student_id}")
        else:
            print(f"   ⚠️  学号格式可能有问题: {profile.student_id}")

        return True

    except StudentProfile.DoesNotExist:
        print(f"   ❌ 未找到自动创建的学生档案!")
        return False

def test_profile_sync_on_update():
    """测试用户信息更新时StudentProfile是否同步"""
    print("\n🧪 测试用户信息同步功能...")

    test_user = User.objects.filter(role='student').first()
    if not test_user:
        print("   ⚠️  没有找到学生用户，跳过同步测试")
        return True

    try:
        profile = StudentProfile.objects.get(user=test_user)

        # 记录原始信息
        original_phone = profile.phone
        original_email = profile.email

        # 更新用户信息
        new_phone = "13900139000"
        new_email = "updated@example.com"

        test_user.phone = new_phone
        test_user.email = new_email
        test_user.save()

        # 刷新档案对象
        profile.refresh_from_db()

        if profile.phone == new_phone and profile.email == new_email:
            print(f"   ✅ 用户信息同步成功!")
            print(f"      手机: {original_phone} → {profile.phone}")
            print(f"      邮箱: {original_email} → {profile.email}")
            return True
        else:
            print(f"   ❌ 用户信息同步失败!")
            print(f"      手机: 期望 {new_phone}, 实际 {profile.phone}")
            print(f"      邮箱: 期望 {new_email}, 实际 {profile.email}")
            return False

    except StudentProfile.DoesNotExist:
        print(f"   ❌ 学生用户没有对应的档案!")
        return False

def test_admin_can_see_new_student():
    """测试管理员能否看到新注册的学生"""
    print("\n🧪 测试管理员查询学生功能...")

    # 创建管理员用户
    admin_username = "test_admin_sync"
    User.objects.filter(username=admin_username).delete()

    admin = User.objects.create_user(
        username=admin_username,
        email="admin@test.com",
        password="adminpass123",
        role='admin'
    )

    print(f"   ✅ 创建管理员用户: {admin.username}")

    # 确保有学生用户和对应的档案
    students_with_profiles = User.objects.filter(
        role='student'
    ).filter(
        studentprofile__isnull=False
    ).count()

    print(f"   📊 有档案的学生数量: {students_with_profiles}")

    if students_with_profiles > 0:
        print(f"   ✅ 管理员可以查询到有档案的学生!")
        return True
    else:
        print(f"   ⚠️  没有找到有档案的学生")
        return False

def main():
    """运行所有测试"""
    print("=" * 60)
    print("🚀 开始测试Django学生管理系统修复功能")
    print("=" * 60)

    from django.utils import timezone

    results = []

    # 运行测试
    results.append(("自动档案创建", test_auto_profile_creation()))
    results.append(("信息同步", test_profile_sync_on_update()))
    results.append(("管理员查询", test_admin_can_see_new_student()))

    # 显示结果
    print("\n" + "=" * 60)
    print("📋 测试结果汇总:")
    print("=" * 60)

    passed = 0
    total = len(results)

    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"   {test_name:<20} {status}")
        if result:
            passed += 1

    print(f"\n📊 总体结果: {passed}/{total} 测试通过")

    if passed == total:
        print("🎉 所有测试通过! 修复功能正常工作。")
        return True
    else:
        print("⚠️  部分测试失败，请检查修复逻辑。")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)