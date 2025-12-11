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
print("ADMIN USER REGISTRATION TEST")
print("=" * 60)

# 创建管理员用户数据
admin_user_data = {
    'username': 'admin2024',
    'first_name': '张',
    'last_name': '管理员',
    'email': 'admin@example.com',
    'phone': '13900139999',
    'role': 'admin',
    'password1': 'Admin123',
    'password2': 'Admin123'
}

print(f"Admin Registration Info:")
print(f"   Username: {admin_user_data['username']}")
print(f"   Name: {admin_user_data['last_name']}{admin_user_data['first_name']}")
print(f"   Email: {admin_user_data['email']}")
print(f"   Role: {admin_user_data['role']}")
print(f"   Password: {admin_user_data['password1']}")
print()

# 创建表单并验证
form = CustomUserCreationForm(data=admin_user_data)

print("Form Validation:")
if form.is_valid():
    print("   [PASS] Form validation successful")

    try:
        # 保存用户
        user = form.save()
        print(f"   [SUCCESS] Admin user created successfully")
        print(f"   User ID: {user.id}")
        print(f"   Username: {user.username}")
        print(f"   Role: {user.role}")
        print(f"   Email: {user.email}")
        print(f"   Created at: {user.created_at}")

        # 测试用户认证
        from django.contrib.auth import authenticate
        print()
        print("Admin Authentication Test:")
        authenticated_user = authenticate(username=admin_user_data['username'],
                                        password=admin_user_data['password1'])
        if authenticated_user:
            print(f"   [SUCCESS] Admin authentication successful")
            print(f"   Authenticated admin: {authenticated_user.username}")
        else:
            print(f"   [FAIL] Admin authentication failed")

        print()
        print("=" * 60)
        print("ADMIN REGISTRATION TEST COMPLETED!")
        print("Admin login credentials:")
        print(f"   Username: {admin_user_data['username']}")
        print(f"   Password: {admin_user_data['password1']}")
        print("=" * 60)

    except Exception as e:
        print(f"   [ERROR] Admin creation failed: {e}")

else:
    print("   [ERROR] Form validation failed:")
    for field, errors in form.errors.items():
        print(f"      {field}: {errors}")

print()
print("Updated System Statistics:")
print(f"   Total users: {User.objects.count()}")
print(f"   Student users: {User.objects.filter(role='student').count()}")
print(f"   Admin users: {User.objects.filter(role='admin').count()}")
print(f"   Teacher users: {User.objects.filter(role='teacher').count()}")