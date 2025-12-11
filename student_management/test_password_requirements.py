#!/usr/bin/env python
import os
import django

# 设置Django设置
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management.settings')
django.setup()

from accounts.forms import CustomUserCreationForm
from accounts.models import User

print("Testing password requirements after adjustments...")
print("=" * 60)

# 测试不同强度的密码
test_cases = [
    {
        'name': '6位简单密码（不与用户名相似）',
        'password': 'Hello123',
        'should_work': True
    },
    {
        'name': '6位纯字母密码',
        'password': 'Helloab',
        'should_work': True
    },
    {
        'name': '6位纯数字密码',
        'password': '123456',
        'should_work': True
    },
    {
        'name': '5位密码（应该失败）',
        'password': 'Hello1',
        'should_work': False
    },
    {
        'name': '8位强密码',
        'password': 'MySecure123',
        'should_work': True
    }
]

base_data = {
    'username': 'testuser456',
    'first_name': '李',
    'last_name': '四',
    'email': 'test456@example.com',
    'phone': '13900139000',
    'role': 'student'
}

success_count = 0
total_count = len(test_cases)

for i, test_case in enumerate(test_cases, 1):
    print(f"\n测试 {i}: {test_case['name']}")
    print(f"密码: {test_case['password']}")

    # 使用不同的用户名避免冲突
    test_data = base_data.copy()
    test_data['username'] = f"testuser{i:03d}"
    test_data['email'] = f"test{i:03d}@example.com"
    test_data['password1'] = test_case['password']
    test_data['password2'] = test_case['password']

    form = CustomUserCreationForm(data=test_data)

    if form.is_valid():
        if test_case['should_work']:
            print("[PASS] Expected success - Got success")
            success_count += 1
        else:
            print("[FAIL] Expected failure - Got success")
    else:
        if not test_case['should_work']:
            print("[PASS] Expected failure - Got failure")
            success_count += 1
        else:
            print("[FAIL] Expected success - Got failure")
            print(f"  Errors: {form.errors}")

        # 清理测试数据（如果已创建）
        if form.is_valid():
            try:
                user = form.save()
                user.delete()
            except:
                pass

print(f"\n" + "=" * 60)
print(f"测试总结:")
print(f"成功: {success_count}/{total_count}")
print(f"成功率: {success_count/total_count*100:.1f}%")

if success_count == total_count:
    print("SUCCESS: All tests passed! Password policy adjustment successful.")
else:
    print("WARNING: Some tests failed, password validators may need further adjustment.")