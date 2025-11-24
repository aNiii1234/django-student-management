import os
import sys
import django

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 配置Django设置
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management.settings')
django.setup()

from accounts.models import User

try:
    # 检查是否有管理员账号
    admin_users = User.objects.filter(role='admin')
    print(f"管理员用户数量: {admin_users.count()}")

    for user in admin_users:
        print(f"用户名: {user.username}, 邮箱: {user.email}, 超级用户: {user.is_superuser}")

    # 检查所有用户
    all_users = User.objects.all()
    print(f"\n总用户数量: {all_users.count()}")

    for user in all_users:
        print(f"用户名: {user.username}, 角色: {user.role}, 活跃: {user.is_active}")

except Exception as e:
    print(f"错误: {e}")