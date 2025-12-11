#!/usr/bin/env python
import os
import django
from django.test import Client

# 设置Django设置
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management.settings')
django.setup()

from django.middleware.csrf import get_token

print("=" * 60)
print("HTTP REGISTRATION TEST")
print("=" * 60)

# 创建Django测试客户端
client = Client()

# 首先获取注册页面以获取CSRF token
print("1. Getting registration page...")
response = client.get('/accounts/register/')
if response.status_code == 200:
    print("   [SUCCESS] Registration page loaded")

    # 提取CSRF token
    csrf_token = get_token(client)
    print(f"   CSRF Token: {csrf_token[:20]}...")

    print()
    print("2. Testing HTTP POST registration...")

    # 准备注册数据
    registration_data = {
        'username': 'http_test_user',
        'first_name': 'HTTP',
        'last_name': '测试',
        'email': 'http_test@example.com',
        'phone': '13700137777',
        'role': 'student',
        'password1': 'Hello123',
        'password2': 'Hello123'
    }

    # 发送注册请求
    response = client.post('/accounts/register/', data=registration_data)

    print(f"   Response Status: {response.status_code}")

    if response.status_code == 302:  # 302 means redirect after successful registration
        print("   [SUCCESS] Registration successful - Redirect detected")

        # 检查是否重定向到登录页面
        if '/accounts/login/' in response.url:
            print("   [SUCCESS] Redirected to login page as expected")

    elif response.status_code == 200:
        print("   [INFO] Registration form returned - checking for errors...")

        # 检查表单是否有错误
        if 'form' in response.context:
            form = response.context['form']
            if form.errors:
                print("   Form errors found:")
                for field, errors in form.errors.items():
                    print(f"      {field}: {errors}")
            else:
                print("   [SUCCESS] Form is valid, checking content...")

        # 检查是否有成功消息
        if response.context and 'messages' in response.context:
            messages = list(response.context['messages'])
            for message in messages:
                print(f"   Message: {message}")
    else:
        print(f"   [ERROR] Unexpected response status: {response.status_code}")
        print(f"   Response content: {response.content[:200]}...")

else:
    print(f"   [ERROR] Failed to load registration page: {response.status_code}")

print()
print("3. Verifying user creation...")
from accounts.models import User
try:
    test_user = User.objects.get(username='http_test_user')
    print(f"   [SUCCESS] User found in database: {test_user.username}")
    print(f"   Email: {test_user.email}")
    print(f"   Role: {test_user.role}")
    print(f"   Created: {test_user.created_at}")

    # 测试登录
    from django.contrib.auth import authenticate
    authenticated_user = authenticate(username='http_test_user', password='Hello123')
    if authenticated_user:
        print("   [SUCCESS] User authentication successful")
    else:
        print("   [ERROR] User authentication failed")

except User.DoesNotExist:
    print("   [ERROR] User not found in database")

print()
print("=" * 60)
print("HTTP REGISTRATION TEST COMPLETED!")
print("=" * 60)