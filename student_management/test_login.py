import os
import sys
import django

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 配置Django设置
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management.settings')
django.setup()

from django.contrib.auth import authenticate
from accounts.models import User

try:
    # 测试用户认证
    print("测试用户认证:")

    # 检查管理员用户
    admin_user = User.objects.get(username='admin')
    print(f"管理员用户存在: {admin_user.username}")
    print(f"邮箱: {admin_user.email}")
    print(f"角色: {admin_user.role}")
    print(f"是否活跃: {admin_user.is_active}")
    print(f"是否超级用户: {admin_user.is_superuser}")

    # 测试认证
    user = authenticate(username='admin', password='admin123')
    if user:
        print("认证成功: 管理员可以登录")
    else:
        print("认证失败: 用户名或密码错误")

    print("\n所有用户列表:")
    for user in User.objects.all():
        print(f"- {user.username} ({user.role}) - 活跃: {user.is_active}")

except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()