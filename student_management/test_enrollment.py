#!/usr/bin/env python
import os
import sys
import django

# 设置Django环境
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management.settings')
django.setup()

from students.models import StudentProfile, Enrollment, Course
from accounts.models import User

# 查找学生用户
student_users = User.objects.filter(role='student')
print(f"找到 {student_users.count()} 个学生用户")

# 查找有学生档案的用户
students = StudentProfile.objects.all()
print(f"找到 {students.count()} 个学生档案")

# 查找选课记录
enrollments = Enrollment.objects.all()
print(f"找到 {enrollments.count()} 个选课记录")

# 显示一些示例数据
if enrollments.exists():
    print("\n最近5个选课记录：")
    for enrollment in enrollments.order_by('-created_at')[:5]:
        print(f"- {enrollment.student.real_name} 选择了 {enrollment.course.name} "
              f"({enrollment.semester} {enrollment.academic_year})")

# 如果没有选课记录，创建一些测试数据
if not enrollments.exists() and students.exists():
    print("\n没有找到选课记录，正在创建测试数据...")

    # 获取第一个学生和第一个课程
    student = students.first()

    # 确保学生有专业
    if not student.major:
        from students.models import Major
        major = Major.objects.first()
        if major:
            student.major = major
            student.save()
            print(f"为学生 {student.real_name} 设置了专业: {major.name}")

    # 创建一些选课记录
    courses = Course.objects.all()[:5]
    from datetime import date

    for i, course in enumerate(courses):
        Enrollment.objects.create(
            student=student,
            course=course,
            major=student.major,
            semester='第一学期' if i % 2 == 0 else '第二学期',
            academic_year=str(2024 if i % 2 == 0 else 2025),
            grade=['A', 'B', 'C'][i % 3] if i > 2 else None,
            score=95 - i * 5 if i > 2 else None
        )
        print(f"+ 创建选课记录: {student.real_name} - {course.name}")

    print(f"\n共创建 {courses.count()} 个选课记录")

# 再次查询
enrollments = Enrollment.objects.all()
print(f"\n当前选课记录总数: {enrollments.count()}")