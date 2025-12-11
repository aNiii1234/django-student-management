#!/usr/bin/env python
import os
import django

# 设置Django设置
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management.settings')
django.setup()

from accounts.forms import CustomUserCreationForm
from accounts.models import User
from students.models import StudentProfile

print("=" * 60)
print("🧪 实时测试注册功能")
print("=" * 60)

# 创建测试用户数据
test_user_data = {
    'username': 'testuser2024',
    'first_name': '王',
    'last_name': '小明',
    'email': 'xiaoming.wang@example.com',
    'phone': '13800138888',
    'role': 'student',
    'password1': 'Hello123',  # 6位密码，符合新要求
    'password2': 'Hello123'
}

print(f"📝 注册用户信息:")
print(f"   用户名: {test_user_data['username']}")
print(f"   姓名: {test_user_data['last_name']}{test_user_data['first_name']}")
print(f"   邮箱: {test_user_data['email']}")
print(f"   手机: {test_user_data['phone']}")
print(f"   角色: {test_user_data['role']}")
print(f"   密码: {test_user_data['password1']}")
print()

# 创建表单并验证
form = CustomUserCreationForm(data=test_user_data)

print("🔍 表单验证结果:")
if form.is_valid():
    print("   ✅ 表单验证通过")

    try:
        # 保存用户
        user = form.save()
        print(f"   ✅ 用户创建成功")
        print(f"   📋 用户ID: {user.id}")
        print(f"   👤 用户名: {user.username}")
        print(f"   🎭 角色: {user.role}")
        print(f"   📧 邮箱: {user.email}")
        print(f"   📱 手机: {user.phone}")
        print(f"   📅 创建时间: {user.created_at}")

        # 检查是否自动创建了StudentProfile
        try:
            profile = StudentProfile.objects.get(user=user)
            print()
            print("🎓 学生档案检查:")
            print(f"   ✅ 学生档案自动创建成功")
            print(f"   🆔 学号: {profile.student_id}")
            print(f"   👨‍🎓 真实姓名: {profile.real_name}")
            print(f"   ⚥ 性别: {profile.get_gender_display()}")
            print(f"   📱 手机: {profile.phone}")
            print(f"   📧 邮箱: {profile.email}")
            print(f"   📅 入学日期: {profile.enrollment_date}")
        except StudentProfile.DoesNotExist:
            print("   ⚠️  学生档案未自动创建")

        # 测试用户认证
        from django.contrib.auth import authenticate
        print()
        print("🔐 用户认证测试:")
        authenticated_user = authenticate(username=test_user_data['username'],
                                        password=test_user_data['password1'])
        if authenticated_user:
            print(f"   ✅ 用户认证成功")
            print(f"   👤 认证用户: {authenticated_user.username}")
        else:
            print(f"   ❌ 用户认证失败")

        print()
        print("=" * 60)
        print("🎉 注册功能测试完成！系统运行正常。")
        print("📝 您可以使用以下信息登录:")
        print(f"   用户名: {test_user_data['username']}")
        print(f"   密码: {test_user_data['password1']}")
        print("=" * 60)

    except Exception as e:
        print(f"   ❌ 用户创建失败: {e}")
        import traceback
        traceback.print_exc()

else:
    print("   ❌ 表单验证失败:")
    for field, errors in form.errors.items():
        print(f"      {field}: {errors}")

print()
print("📊 当前系统统计:")
print(f"   总用户数: {User.objects.count()}")
print(f"   学生用户数: {User.objects.filter(role='student').count()}")
print(f"   管理员数: {User.objects.filter(role='admin').count()}")
print(f"   教师数: {User.objects.filter(role='teacher').count()}")
print(f"   学生档案数: {StudentProfile.objects.count()}")