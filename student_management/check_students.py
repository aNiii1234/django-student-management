import os
import sys
import django

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 配置Django设置
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management.settings')
django.setup()

from accounts.models import User
from students.models import StudentProfile

print("=== 系统用户和档案情况 ===")

# 显示所有用户
print("\n所有用户:")
for user in User.objects.all():
    print(f"用户名: {user.username}")
    print(f"  - 角色: {user.get_role_display}")
    print(f"  - 邮箱: {user.email}")
    print(f"  - 活跃: {user.is_active}")

    # 如果是学生，检查是否有学生档案
    if user.role == 'student':
        try:
            profile = StudentProfile.objects.get(user=user)
            print(f"  - 学生档案: 存在 (学号: {profile.student_id})")
        except StudentProfile.DoesNotExist:
            print(f"  - 学生档案: 不存在")

# 显示所有学生档案
print("\n所有学生档案:")
for profile in StudentProfile.objects.all():
    print(f"学号: {profile.student_id}")
    print(f"  - 姓名: {profile.real_name}")
    print(f"  - 关联用户: {profile.user.username}")
    print(f"  - 性别: {profile.get_gender_display}")