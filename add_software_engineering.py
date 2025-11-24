#!/usr/bin/env python
import os
import sys
import django

# 设置Django环境
sys.path.append('D:/PBLceshi/student_management')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management.settings')
django.setup()

from students.models import Department, Major

def add_software_engineering_major():
    # 查找计算机科学与技术学院
    try:
        cs_department = Department.objects.get(name='计算机科学与技术学院')
        print(f"找到院系: {cs_department.name}")
    except Department.DoesNotExist:
        print("未找到计算机科学与技术学院，先创建该学院...")
        cs_department = Department.objects.create(
            name='计算机科学与技术学院',
            description='计算机科学与技术学院负责计算机相关专业的教学和研究'
        )
        print(f"创建院系: {cs_department.name}")

    # 检查软件工程专业是否已存在
    try:
        software_major = Major.objects.get(name='软件工程')
        print(f"软件工程专业已存在: {software_major.name}")
        return software_major
    except Major.DoesNotExist:
        print("创建软件工程专业...")
        software_major = Major.objects.create(
            name='软件工程',
            department=cs_department,
            description='软件工程专业培养软件设计、开发和管理的高级人才'
        )
        print(f"创建专业: {software_major.name} - 所属院系: {software_major.department.name}")
        return software_major

def show_current_data():
    print("\n当前院系和专业数据:")
    departments = Department.objects.all()
    for dept in departments:
        print(f"\n院系: {dept.name}")
        majors = dept.major_set.all()
        for major in majors:
            print(f"  - 专业: {major.name}")

if __name__ == '__main__':
    print("开始添加软件工程专业...")
    software_major = add_software_engineering_major()
    show_current_data()
    print("\n操作完成！")