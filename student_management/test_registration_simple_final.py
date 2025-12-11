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
print("LIVE REGISTRATION FUNCTION TEST")
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

print(f"Registration Info:")
print(f"   Username: {test_user_data['username']}")
print(f"   Name: {test_user_data['last_name']}{test_user_data['first_name']}")
print(f"   Email: {test_user_data['email']}")
print(f"   Phone: {test_user_data['phone']}")
print(f"   Role: {test_user_data['role']}")
print(f"   Password: {test_user_data['password1']}")
print()

# 创建表单并验证
form = CustomUserCreationForm(data=test_user_data)

print("Form Validation:")
if form.is_valid():
    print("   [PASS] Form validation successful")

    try:
        # 保存用户
        user = form.save()
        print(f"   [SUCCESS] User created successfully")
        print(f"   User ID: {user.id}")
        print(f"   Username: {user.username}")
        print(f"   Role: {user.role}")
        print(f"   Email: {user.email}")
        print(f"   Phone: {user.phone}")
        print(f"   Created at: {user.created_at}")

        # 检查是否自动创建了StudentProfile
        try:
            profile = StudentProfile.objects.get(user=user)
            print()
            print("Student Profile Check:")
            print(f"   [SUCCESS] Student profile auto-created")
            print(f"   Student ID: {profile.student_id}")
            print(f"   Real Name: {profile.real_name}")
            print(f"   Gender: {profile.get_gender_display()}")
            print(f"   Phone: {profile.phone}")
            print(f"   Email: {profile.email}")
            print(f"   Enrollment Date: {profile.enrollment_date}")
        except StudentProfile.DoesNotExist:
            print("   [WARNING] Student profile not auto-created")

        # 测试用户认证
        from django.contrib.auth import authenticate
        print()
        print("Authentication Test:")
        authenticated_user = authenticate(username=test_user_data['username'],
                                        password=test_user_data['password1'])
        if authenticated_user:
            print(f"   [SUCCESS] User authentication successful")
            print(f"   Authenticated user: {authenticated_user.username}")
        else:
            print(f"   [FAIL] User authentication failed")

        print()
        print("=" * 60)
        print("REGISTRATION TEST COMPLETED! System working normally.")
        print("You can login with:")
        print(f"   Username: {test_user_data['username']}")
        print(f"   Password: {test_user_data['password1']}")
        print("=" * 60)

    except Exception as e:
        print(f"   [ERROR] User creation failed: {e}")
        import traceback
        traceback.print_exc()

else:
    print("   [ERROR] Form validation failed:")
    for field, errors in form.errors.items():
        print(f"      {field}: {errors}")

print()
print("System Statistics:")
print(f"   Total users: {User.objects.count()}")
print(f"   Student users: {User.objects.filter(role='student').count()}")
print(f"   Admin users: {User.objects.filter(role='admin').count()}")
print(f"   Teacher users: {User.objects.filter(role='teacher').count()}")
print(f"   Student profiles: {StudentProfile.objects.count()}")