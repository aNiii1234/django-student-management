#!/usr/bin/env python
import os
import django

# 设置Django设置
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management.settings')
django.setup()

from accounts.forms import CustomUserCreationForm
from accounts.models import User

print("Testing registration functionality...")

# 测试表单
test_data = {
    'username': 'testuser123',
    'first_name': '张',
    'last_name': '三',
    'email': 'test@example.com',
    'phone': '13800138000',
    'role': 'student',
    'password1': 'Test123',
    'password2': 'Test123'
}

form = CustomUserCreationForm(data=test_data)
print(f"Form valid: {form.is_valid()}")

if not form.is_valid():
    print("Form errors:")
    for field, errors in form.errors.items():
        print(f"  {field}: {errors}")
else:
    print("Form validation successful!")

    # 尝试保存用户
    try:
        user = form.save()
        print(f"User created: {user.username} (ID: {user.id})")

        # 清理测试数据
        user.delete()
        print("Test data cleaned up")
    except Exception as e:
        print(f"Error saving user: {e}")