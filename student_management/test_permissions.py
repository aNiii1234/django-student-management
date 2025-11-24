import os
import sys
import django

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 配置Django设置
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management.settings')
django.setup()

from django.test import Client
from accounts.models import User

print("=== 测试用户权限分离 ===")

# 创建测试客户端
client = Client()

# 测试未登录用户访问
print("\n1. 未登录用户测试:")
response = client.get('/')
print(f"访问首页 -> 状态码: {response.status_code} (应该重定向到登录页)")

response = client.get('/accounts/admin_dashboard/')
print(f"访问管理员面板 -> 状态码: {response.status_code} (应该重定向到登录页)")

response = client.get('/accounts/student_dashboard/')
print(f"访问学生面板 -> 状态码: {response.status_code} (应该重定向到登录页)")

# 测试管理员登录
print("\n2. 管理员权限测试:")
admin_logged_in = client.login(username='admin', password='admin123')
print(f"管理员登录: {'成功' if admin_logged_in else '失败'}")

if admin_logged_in:
    response = client.get('/accounts/admin_dashboard/')
    print(f"访问管理员面板 -> 状态码: {response.status_code} (应该200 OK)")

    response = client.get('/accounts/student_dashboard/')
    print(f"访问学生面板 -> 状态码: {response.status_code} (应该重定向到管理员面板)")

    response = client.get('/students/student_profile_list/')
    print(f"访问学生管理 -> 状态码: {response.status_code} (应该200 OK)")

# 注销管理员
client.logout()

# 测试学生登录
print("\n3. 学生权限测试:")
student_logged_in = client.login(username='2024001', password='student123')
print(f"学生登录: {'成功' if student_logged_in else '失败'}")

if student_logged_in:
    response = client.get('/accounts/student_dashboard/')
    print(f"访问学生面板 -> 状态码: {response.status_code} (应该200 OK)")

    response = client.get('/accounts/admin_dashboard/')
    print(f"访问管理员面板 -> 状态码: {response.status_code} (应该重定向到首页)")

    response = client.get('/students/student_profile_list/')
    print(f"访问学生管理 -> 状态码: {response.status_code} (应该重定向到首页)")

    response = client.get('/students/my_enrollments/')
    print(f"访问我的课程 -> 状态码: {response.status_code} (应该200 OK)")

# 注销学生
client.logout()

print("\n=== 权限分离测试完成 ===")
print("\n登录方式总结:")
print("1. 管理员登录:")
print("   - 访问: http://127.0.0.1:8000/accounts/login/")
print("   - 用户名: admin")
print("   - 密码: admin123")
print("   - 登录后自动跳转到管理员面板")

print("\n2. 学生登录:")
print("   - 访问: http://127.0.0.1:8000/accounts/login/")
print("   - 用户名: 2024001 或 2024002")
print("   - 密码: student123")
print("   - 登录后自动跳转到学生面板")

print("\n3. 新学生注册:")
print("   - 访问: http://127.0.0.1:8000/accounts/register/")
print("   - 填写注册信息，角色选择'学生'")
print("   - 管理员在后台创建完整的学生档案")

print("\n权限控制机制:")
print("- 视图函数使用@login_required装饰器要求登录")
print("- 管理员功能使用AdminRequiredMixin检查role=='admin'")
print("- 学生功能检查role=='student'")
print("- URL重定向根据用户角色自动跳转")