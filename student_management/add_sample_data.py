#!/usr/bin/env python
import os
import sys
import django

# 设置Django环境
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management.settings')
django.setup()

from students.models import Department, Major, Course

# 清空现有数据（可选）
print("正在清空现有数据...")
Department.objects.all().delete()
Major.objects.all().delete()
Course.objects.all().delete()

# 1. 添加院系数据
print("\n正在添加院系数据...")
departments = [
    {
        'name': '计算机科学与技术学院',
        'code': 'CS',
        'description': '负责计算机科学、软件工程、人工智能等相关专业的教学和科研工作',
        'head_name': '王院长',
        'phone': '0123-45678901'
    },
    {
        'name': '电子信息工程学院',
        'code': 'EI',
        'description': '致力于电子工程、通信工程、微电子等领域的教学与研究',
        'head_name': '李院长',
        'phone': '0123-45678902'
    },
    {
        'name': '机械工程学院',
        'code': 'ME',
        'description': '培养机械设计制造、自动化、车辆工程等领域的专业人才',
        'head_name': '张院长',
        'phone': '0123-45678903'
    },
    {
        'name': '经济管理学院',
        'code': 'EM',
        'description': '涵盖经济学、管理学、金融学等多个商科专业',
        'head_name': '刘院长',
        'phone': '0123-45678904'
    },
    {
        'name': '外国语学院',
        'code': 'FL',
        'description': '提供英语、日语、法语等多种语言的教学和研究',
        'head_name': '陈院长',
        'phone': '0123-45678905'
    },
    {
        'name': '数学与物理学院',
        'code': 'MP',
        'description': '承担基础数学、应用数学、物理学等基础学科的教学',
        'head_name': '赵院长',
        'phone': '0123-45678906'
    }
]

created_departments = {}
for dept_data in departments:
    dept = Department.objects.create(**dept_data)
    created_departments[dept.code] = dept
    print(f"  [创建] 院系: {dept.name}")

# 2. 添加专业数据
print("\n正在添加专业数据...")
majors = [
    # 计算机科学与技术学院的专业
    {
        'name': '计算机科学与技术',
        'code': 'CS001',
        'department': created_departments['CS'],
        'duration': 4,
        'description': '培养计算机系统设计、开发和应用的高级专门人才'
    },
    {
        'name': '软件工程',
        'code': 'CS002',
        'department': created_departments['CS'],
        'duration': 4,
        'description': '专注于软件系统开发、测试和维护的工程专业'
    },
    {
        'name': '人工智能',
        'code': 'CS003',
        'department': created_departments['CS'],
        'duration': 4,
        'description': '研究机器学习、深度学习、自然语言处理等AI技术'
    },
    {
        'name': '数据科学与大数据技术',
        'code': 'CS004',
        'department': created_departments['CS'],
        'duration': 4,
        'description': '培养数据采集、处理、分析和可视化的专业人才'
    },

    # 电子信息工程学院的专业
    {
        'name': '电子信息工程',
        'code': 'EI001',
        'department': created_departments['EI'],
        'duration': 4,
        'description': '研究信息获取、传输、处理和应用的工程技术'
    },
    {
        'name': '通信工程',
        'code': 'EI002',
        'department': created_departments['EI'],
        'duration': 4,
        'description': '培养通信系统设计、开发和管理的高级人才'
    },
    {
        'name': '微电子科学与工程',
        'code': 'EI003',
        'department': created_departments['EI'],
        'duration': 4,
        'description': '研究半导体器件、集成电路设计和制造'
    },

    # 机械工程学院的专业
    {
        'name': '机械设计制造及其自动化',
        'code': 'ME001',
        'department': created_departments['ME'],
        'duration': 4,
        'description': '培养机械设计、制造及自动化控制的专业人才'
    },
    {
        'name': '车辆工程',
        'code': 'ME002',
        'department': created_departments['ME'],
        'duration': 4,
        'description': '专注于汽车设计、制造和检测技术'
    },
    {
        'name': '工业工程',
        'code': 'ME003',
        'department': created_departments['ME'],
        'duration': 4,
        'description': '优化生产系统、提高生产效率的工程学科'
    },

    # 经济管理学院的专业
    {
        'name': '工商管理',
        'code': 'EM001',
        'department': created_departments['EM'],
        'duration': 4,
        'description': '培养企业管理、市场营销等方面的高级管理人才'
    },
    {
        'name': '会计学',
        'code': 'EM002',
        'department': created_departments['EM'],
        'duration': 4,
        'description': '专注于会计核算、财务管理和审计工作'
    },
    {
        'name': '金融工程',
        'code': 'EM003',
        'department': created_departments['EM'],
        'duration': 4,
        'description': '运用数理方法和工程技术开发金融产品和服务'
    },

    # 外国语学院的专业
    {
        'name': '英语',
        'code': 'FL001',
        'department': created_departments['FL'],
        'duration': 4,
        'description': '培养英语听、说、读、写、译全面发展的专业人才'
    },
    {
        'name': '日语',
        'code': 'FL002',
        'department': created_departments['FL'],
        'duration': 4,
        'description': '培养日语语言文学和应用日语的专业人才'
    },
    {
        'name': '商务英语',
        'code': 'FL003',
        'department': created_departments['FL'],
        'duration': 4,
        'description': '结合商务知识和英语应用的复合型专业'
    },

    # 数学与物理学院的专业
    {
        'name': '数学与应用数学',
        'code': 'MP001',
        'department': created_departments['MP'],
        'duration': 4,
        'description': '培养数学理论研究和应用的专业人才'
    },
    {
        'name': '应用物理学',
        'code': 'MP002',
        'department': created_departments['MP'],
        'duration': 4,
        'description': '将物理学原理应用于工程技术领域的专业'
    }
]

created_majors = {}
for major_data in majors:
    major = Major.objects.create(**major_data)
    created_majors[major.code] = major
    print(f"  [创建] 专业: {major.name} ({major.department.name})")

# 3. 添加课程数据
print("\n正在添加课程数据...")
courses = [
    # 计算机相关课程
    {
        'name': '高等数学',
        'code': 'MATH001',
        'course_type': 'required',
        'credits': 5.0,
        'hours': 80,
        'description': '微积分、线性代数等高等数学基础'
    },
    {
        'name': '程序设计基础',
        'code': 'CS101',
        'course_type': 'required',
        'credits': 4.0,
        'hours': 64,
        'description': 'C语言程序设计基础'
    },
    {
        'name': '数据结构与算法',
        'code': 'CS201',
        'course_type': 'required',
        'credits': 4.0,
        'hours': 64,
        'description': '常用数据结构和算法设计与分析'
    },
    {
        'name': '计算机网络',
        'code': 'CS301',
        'course_type': 'required',
        'credits': 3.0,
        'hours': 48,
        'description': '计算机网络原理与技术'
    },
    {
        'name': '操作系统',
        'code': 'CS302',
        'course_type': 'required',
        'credits': 3.0,
        'hours': 48,
        'description': '操作系统原理与设计'
    },
    {
        'name': '数据库系统',
        'code': 'CS303',
        'course_type': 'required',
        'credits': 3.0,
        'hours': 48,
        'description': '数据库原理与应用'
    },
    {
        'name': '机器学习',
        'code': 'CS401',
        'course_type': 'elective',
        'credits': 3.0,
        'hours': 48,
        'description': '机器学习算法与应用'
    },
    {
        'name': '深度学习',
        'code': 'CS402',
        'course_type': 'elective',
        'credits': 3.0,
        'hours': 48,
        'description': '深度学习理论与框架应用'
    },

    # 电子信息相关课程
    {
        'name': '电路分析基础',
        'code': 'EE101',
        'course_type': 'required',
        'credits': 4.0,
        'hours': 64,
        'description': '基本电路理论与分析方法'
    },
    {
        'name': '模拟电子技术',
        'code': 'EE201',
        'course_type': 'required',
        'credits': 4.0,
        'hours': 64,
        'description': '模拟电路设计与分析'
    },
    {
        'name': '数字电子技术',
        'code': 'EE202',
        'course_type': 'required',
        'credits': 4.0,
        'hours': 64,
        'description': '数字逻辑电路设计'
    },
    {
        'name': '信号与系统',
        'code': 'EE301',
        'course_type': 'required',
        'credits': 3.0,
        'hours': 48,
        'description': '信号处理与系统分析'
    },
    {
        'name': '通信原理',
        'code': 'EE302',
        'course_type': 'required',
        'credits': 3.0,
        'hours': 48,
        'description': '现代通信系统原理'
    },

    # 机械相关课程
    {
        'name': '工程图学',
        'code': 'ME101',
        'course_type': 'required',
        'credits': 3.0,
        'hours': 48,
        'description': '工程制图与CAD技术'
    },
    {
        'name': '理论力学',
        'code': 'ME201',
        'course_type': 'required',
        'credits': 4.0,
        'hours': 64,
        'description': '静力学、运动学和动力学'
    },
    {
        'name': '材料力学',
        'code': 'ME202',
        'course_type': 'required',
        'credits': 3.0,
        'hours': 48,
        'description': '材料性能与强度分析'
    },
    {
        'name': '机械设计',
        'code': 'ME301',
        'course_type': 'required',
        'credits': 4.0,
        'hours': 64,
        'description': '机械零件设计原理'
    },
    {
        'name': '制造技术基础',
        'code': 'ME302',
        'course_type': 'required',
        'credits': 3.0,
        'hours': 48,
        'description': '机械制造工艺与设备'
    },

    # 经管相关课程
    {
        'name': '微观经济学',
        'code': 'EC101',
        'course_type': 'required',
        'credits': 3.0,
        'hours': 48,
        'description': '微观经济理论与应用'
    },
    {
        'name': '宏观经济学',
        'code': 'EC102',
        'course_type': 'required',
        'credits': 3.0,
        'hours': 48,
        'description': '宏观经济理论与政策'
    },
    {
        'name': '管理学原理',
        'code': 'MG101',
        'course_type': 'required',
        'credits': 3.0,
        'hours': 48,
        'description': '现代管理理论与方法'
    },
    {
        'name': '市场营销学',
        'code': 'MG201',
        'course_type': 'required',
        'credits': 3.0,
        'hours': 48,
        'description': '市场营销策略与管理'
    },
    {
        'name': '财务会计',
        'code': 'AC101',
        'course_type': 'required',
        'credits': 4.0,
        'hours': 64,
        'description': '会计核算与财务报表'
    },
    {
        'name': '统计学',
        'code': 'ST101',
        'course_type': 'required',
        'credits': 3.0,
        'hours': 48,
        'description': '统计理论与方法应用'
    },

    # 外语相关课程
    {
        'name': '综合英语',
        'code': 'EN101',
        'course_type': 'required',
        'credits': 4.0,
        'hours': 64,
        'description': '英语听说读写综合训练'
    },
    {
        'name': '英语听力',
        'code': 'EN102',
        'course_type': 'required',
        'credits': 2.0,
        'hours': 32,
        'description': '英语听力技能训练'
    },
    {
        'name': '英语口语',
        'code': 'EN103',
        'course_type': 'required',
        'credits': 2.0,
        'hours': 32,
        'description': '英语口语交流训练'
    },
    {
        'name': '英美文学',
        'code': 'EN201',
        'course_type': 'elective',
        'credits': 2.0,
        'hours': 32,
        'description': '英国与美国文学作品选读'
    },
    {
        'name': '商务日语',
        'code': 'JP101',
        'course_type': 'elective',
        'credits': 3.0,
        'hours': 48,
        'description': '商务场合日语应用'
    },

    # 数学物理相关课程
    {
        'name': '线性代数',
        'code': 'MATH201',
        'course_type': 'required',
        'credits': 3.0,
        'hours': 48,
        'description': '线性方程组与矩阵理论'
    },
    {
        'name': '概率论与数理统计',
        'code': 'MATH202',
        'course_type': 'required',
        'credits': 3.0,
        'hours': 48,
        'description': '概率理论与统计方法'
    },
    {
        'name': '大学物理',
        'code': 'PHY101',
        'course_type': 'required',
        'credits': 4.0,
        'hours': 64,
        'description': '力学、热学、电磁学等物理基础'
    },
    {
        'name': '物理实验',
        'code': 'PHY102',
        'course_type': 'required',
        'credits': 1.0,
        'hours': 32,
        'description': '基础物理实验'
    },
    {
        'name': '复变函数',
        'code': 'MATH301',
        'course_type': 'elective',
        'credits': 2.0,
        'hours': 32,
        'description': '复变函数理论'
    },
    {
        'name': '数学建模',
        'code': 'MATH302',
        'course_type': 'elective',
        'credits': 2.0,
        'hours': 32,
        'description': '数学建模方法与实践'
    },

    # 实践课程
    {
        'name': '计算机程序设计实验',
        'code': 'LAB101',
        'course_type': 'practical',
        'credits': 1.0,
        'hours': 32,
        'description': '程序设计上机实践'
    },
    {
        'name': '电子工艺实习',
        'code': 'LAB201',
        'course_type': 'practical',
        'credits': 2.0,
        'hours': 64,
        'description': '电子产品制作实践'
    },
    {
        'name': '金工实习',
        'code': 'LAB301',
        'course_type': 'practical',
        'credits': 2.0,
        'hours': 64,
        'description': '机械加工实践训练'
    },
    {
        'name': '社会调查',
        'code': 'PRACT101',
        'course_type': 'practical',
        'credits': 1.0,
        'hours': 32,
        'description': '社会调查方法与实践'
    },
    {
        'name': '毕业设计',
        'code': 'GRADUATE',
        'course_type': 'required',
        'credits': 8.0,
        'hours': 128,
        'description': '毕业设计（论文）'
    }
]

created_courses = {}
for course_data in courses:
    course = Course.objects.create(**course_data)
    created_courses[course.code] = course
    print(f"  [创建] 课程: {course.name} ({course.get_course_type_display()}, {course.credits}学分)")

# 打印统计信息
print("\n[完成] 数据添加完成！")
print(f"院系数量: {Department.objects.count()}")
print(f"专业数量: {Major.objects.count()}")
print(f"课程数量: {Course.objects.count()}")
print(f"必修课: {Course.objects.filter(course_type='required').count()}")
print(f"选修课: {Course.objects.filter(course_type='elective').count()}")
print(f"实践课: {Course.objects.filter(course_type='practical').count()}")