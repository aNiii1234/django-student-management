#!/usr/bin/env python
import os
import sys
import django
from datetime import date, timedelta

# 设置Django环境
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management.settings')
django.setup()

from students.models import StudentProfile, Department, Major, Enrollment, Course
from accounts.models import User

# 创建或更新学生档案
def create_student_profile():
    # 查找student用户
    try:
        student_user = User.objects.get(username='student', role='student')
    except User.DoesNotExist:
        # 如果不存在，创建一个
        student_user = User.objects.create_user(
            username='student',
            email='student@example.com',
            password='123456',
            role='student',
            real_name='测试学生'
        )
        print(f"创建了学生用户: {student_user.username}")

    # 获取计算机科学与技术专业
    try:
        department = Department.objects.get(name='计算机科学与技术学院')
        major = Major.objects.get(name='计算机科学与技术', department=department)
    except:
        print("未找到计算机科学与技术专业")
        return None

    # 创建或更新学生档案
    student_profile, created = StudentProfile.objects.update_or_create(
        user=student_user,
        defaults={
            'student_id': '2024001',
            'real_name': '张三',
            'gender': 'M',
            'birth_date': date(2002, 5, 15),
            'department': department,
            'major': major,
            'enrollment_date': date(2024, 9, 1),
            'graduation_date': date(2028, 6, 30),
            'class_name': '计科2401',
            'phone': '13800138000',
            'email': 'zhangsan@example.com',
        }
    )

    if created:
        print(f"创建了学生档案: {student_profile.real_name}")
    else:
        print(f"更新了学生档案: {student_profile.real_name}")

    return student_profile

# 创建选课记录
def create_enrollments(student_profile):
    # 删除该学生现有的选课记录
    Enrollment.objects.filter(student=student_profile).delete()
    print(f"删除了 {student_profile.real_name} 的所有选课记录")

    # 获取一些课程
    courses = Course.objects.all()[:6]

    enrollments_data = [
        (courses[0], '第一学期', '2024', None, None),  # 进行中的课程
        (courses[1], '第一学期', '2024', None, None),  # 进行中的课程
        (courses[2], '第一学期', '2024', None, None),  # 进行中的课程
        (courses[3], '第一学期', '2024', 'A', 95.0),   # 已完成的课程
        (courses[4], '第一学期', '2024', 'B', 85.0),   # 已完成的课程
        (courses[5], '第二学期', '2024', None, None),  # 进行中的课程
    ]

    for course, semester, academic_year, grade, score in enrollments_data:
        Enrollment.objects.create(
            student=student_profile,
            course=course,
            major=student_profile.major,
            semester=semester,
            academic_year=academic_year,
            grade=grade,
            score=score
        )
        status = f"({grade})" if grade else "(进行中)"
        print(f"+ 选课: {course.name} {status}")

# 执行创建
if __name__ == '__main__':
    print("设置学生数据...")
    student_profile = create_student_profile()

    if student_profile:
        create_enrollments(student_profile)
        print("\n设置完成！")
        print(f"学生 {student_profile.real_name} 的信息:")
        print(f"- 学号: {student_profile.student_id}")
        print(f"- 性别: {student_profile.get_gender_display()}")
        print(f"- 年龄: {student_profile.age}岁")
        print(f"- 学院: {student_profile.department.name}")
        print(f"- 专业: {student_profile.major.name}")

        enrollments = Enrollment.objects.filter(student=student_profile)
        print(f"\n选课记录 ({enrollments.count()} 门):")
        for e in enrollments:
            status = f"成绩: {e.get_grade_display}" if e.grade else "进行中"
            print(f"- {e.course.name} ({e.semester} {e.academic_year}) - {status}")