import os
import sys
import django

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 配置Django设置
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management.settings')
django.setup()

from accounts.models import User
from students.models import StudentProfile, Department, Major, Course

print("=== 创建演示学生用户 ===")

# 检查是否需要创建基础数据
print("\n1. 检查基础数据...")

# 创建院系
dept, created = Department.objects.get_or_create(
    code='CS',
    defaults={
        'name': '计算机科学学院',
        'description': '计算机科学相关专业的院系',
        'head_name': '张教授',
        'phone': '010-12345678'
    }
)
if created:
    print("  - 创建院系: 计算机科学学院")
else:
    print("  - 院系已存在: 计算机科学学院")

# 创建专业
major, created = Major.objects.get_or_create(
    code='CS001',
    defaults={
        'name': '计算机科学与技术',
        'department': dept,
        'duration': 4,
        'description': '计算机科学与技术专业'
    }
)
if created:
    print("  - 创建专业: 计算机科学与技术")
else:
    print("  - 专业已存在: 计算机科学与技术")

# 创建课程
course1, created = Course.objects.get_or_create(
    code='CS101',
    defaults={
        'name': '程序设计基础',
        'course_type': 'required',
        'credits': 4.0,
        'hours': 64,
        'description': 'Python程序设计基础课程'
    }
)
if created:
    print("  - 创建课程: 程序设计基础")
else:
    print("  - 课程已存在: 程序设计基础")

course2, created = Course.objects.get_or_create(
    code='CS102',
    defaults={
        'name': '数据结构',
        'course_type': 'required',
        'credits': 4.0,
        'hours': 64,
        'description': '数据结构与算法课程'
    }
)
if created:
    print("  - 创建课程: 数据结构")
else:
    print("  - 课程已存在: 数据结构")

print("\n2. 创建演示学生...")

# 创建演示学生
demo_students = [
    {
        'username': '2024001',
        'password': 'student123',
        'email': '2024001@student.edu.cn',
        'first_name': '张',
        'last_name': '三',
        'student_id': '2024001',
        'real_name': '张三',
        'gender': 'M',
        'birth_date': '2003-05-15',
        'id_card_number': '110101200305150001',
        'nationality': '汉族',
        'phone': '13800138001',
        'email': 'zhangsan@example.com',
        'enrollment_date': '2023-09-01',
        'graduation_date': '2027-06-30',
        'class_name': '计科2101班',
        'enrollment_status': 'enrolled',
        'political_status': 'league_member',
        'address': '北京市海淀区中关村南大街5号',
        'emergency_contact': '张父',
        'emergency_phone': '13900139001',
        'emergency_relation': '父亲',
        'emergency_contact2': '张母',
        'emergency_phone2': '13900139002',
        'emergency_relation2': '母亲'
    },
    {
        'username': '2024002',
        'password': 'student123',
        'email': '2024002@student.edu.cn',
        'first_name': '李',
        'last_name': '四',
        'student_id': '2024002',
        'real_name': '李四',
        'gender': 'F',
        'birth_date': '2003-08-20',
        'id_card_number': '310101200308200002',
        'nationality': '汉族',
        'phone': '13900139002',
        'email': 'lisi@example.com',
        'enrollment_date': '2023-09-01',
        'graduation_date': '2027-06-30',
        'class_name': '计科2102班',
        'enrollment_status': 'enrolled',
        'political_status': 'league_member',
        'address': '上海市浦东新区世纪大道100号',
        'emergency_contact': '李母',
        'emergency_phone': '13800138002',
        'emergency_relation': '母亲',
        'emergency_contact2': '',
        'emergency_phone2': '',
        'emergency_relation2': ''
    }
]

for student_data in demo_students:
    # 创建用户账号
    user, created = User.objects.get_or_create(
        username=student_data['username'],
        defaults={
            'email': student_data['email'],
            'first_name': student_data['first_name'],
            'last_name': student_data['last_name'],
            'role': 'student'
        }
    )

    if created:
        user.set_password(student_data['password'])
        user.save()
        print(f"  - 创建用户: {student_data['username']}")

        # 创建学生档案
        profile = StudentProfile.objects.create(
            user=user,
            student_id=student_data['student_id'],
            real_name=student_data['real_name'],
            gender=student_data['gender'],
            birth_date=student_data['birth_date'],
            id_card_number=student_data['id_card_number'],
            nationality=student_data['nationality'],
            phone=student_data['phone'],
            email=student_data['email'],
            enrollment_date=student_data['enrollment_date'],
            graduation_date=student_data['graduation_date'],
            class_name=student_data['class_name'],
            enrollment_status=student_data['enrollment_status'],
            political_status=student_data['political_status'],
            address=student_data['address'],
            emergency_contact=student_data['emergency_contact'],
            emergency_phone=student_data['emergency_phone'],
            emergency_relation=student_data['emergency_relation'],
            emergency_contact2=student_data['emergency_contact2'],
            emergency_phone2=student_data['emergency_phone2'],
            emergency_relation2=student_data['emergency_relation2'],
            department=dept,
            major=major
        )
        print(f"  - 创建学生档案: {student_data['real_name']} ({student_data['student_id']})")
    else:
        print(f"  - 用户已存在: {student_data['username']}")

print("\n=== 学生用户创建完成 ===")
print("\n学生登录信息:")
print("学生1:")
print("  用户名: 2024001")
print("  密码: student123")
print("  姓名: 张三")
print("  学号: 2024001")

print("\n学生2:")
print("  用户名: 2024002")
print("  密码: student123")
print("  姓名: 李四")
print("  学号: 2024002")

print("\n=== 权限分离说明 ===")
print("管理员权限:")
print("  - 可以访问所有管理页面")
print("  - 可以管理用户、院系、专业、课程")
print("  - 可以管理学生档案和成绩")
print("  - 访问管理员面板")

print("\n学生权限:")
print("  - 只能访问自己的资料和选课信息")
print("  - 可以编辑个人基本信息")
print("  - 可以查看自己的课程和成绩")
print("  - 无法访问其他学生的信息")
print("  - 访问学生面板")