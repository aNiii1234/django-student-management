import os
import sys
import django

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 配置Django设置
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management.settings')
django.setup()

try:
    from django.urls import reverse

    # 测试各个URL
    print("测试URL配置:")

    # 测试accounts应用URL
    try:
        login_url = reverse('accounts:login')
        print(f"OK 登录页面: {login_url}")
    except Exception as e:
        print(f"ERROR 登录页面错误: {e}")

    try:
        admin_dashboard_url = reverse('accounts:admin_dashboard')
        print(f"OK 管理员面板: {admin_dashboard_url}")
    except Exception as e:
        print(f"ERROR 管理员面板错误: {e}")

    try:
        student_dashboard_url = reverse('accounts:student_dashboard')
        print(f"OK 学生面板: {student_dashboard_url}")
    except Exception as e:
        print(f"ERROR 学生面板错误: {e}")

    try:
        profile_url = reverse('accounts:profile')
        print(f"OK 个人资料: {profile_url}")
    except Exception as e:
        print(f"ERROR 个人资料错误: {e}")

    # 测试students应用URL
    try:
        home_url = reverse('students:home')
        print(f"OK 首页: {home_url}")
    except Exception as e:
        print(f"ERROR 首页错误: {e}")

    print("\nOK 所有URL配置测试完成!")

except Exception as e:
    print(f"ERROR URL配置测试失败: {e}")
    import traceback
    traceback.print_exc()