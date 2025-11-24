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
    # 创建超级管理员
    User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123',
        first_name='管理',
        last_name='员',
        role='admin'
    )
    print("管理员账号创建成功！")
    print("用户名: admin")
    print("密码: admin123")
except Exception as e:
    print(f"创建管理员失败: {e}")
    print("管理员可能已存在")