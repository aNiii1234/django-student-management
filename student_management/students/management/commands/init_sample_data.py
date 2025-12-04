from django.core.management.base import BaseCommand
from django.db import transaction
from students.models import Department, Major, Course

class Command(BaseCommand):
    help = '初始化示例数据：院系、专业和课程'

    def handle(self, *args, **kwargs):
        self.stdout.write('开始初始化示例数据...')

        try:
            with transaction.atomic():
                # 创建院系数据
                departments = self.create_departments()

                # 创建专业数据
                majors = self.create_majors(departments)

                # 创建课程数据
                courses = self.create_courses(majors)

                self.stdout.write(
                    self.style.SUCCESS(
                        f'成功初始化数据！\n'
                        f'院系: {len(departments)} 个\n'
                        f'专业: {len(majors)} 个\n'
                        f'课程: {len(courses)} 个'
                    )
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'初始化数据失败: {e}')
            )

    def create_departments(self):
        """创建院系数据"""
        departments_data = [
            {
                'name': '计算机科学与技术学院',
                'code': 'CS',
                'description': '培养计算机领域专业人才，涵盖软件开发、人工智能、网络安全等方向',
                'head_name': '张教授',
                'phone': '0123-45678901'
            },
            {
                'name': '电子信息工程学院',
                'code': 'EE',
                'description': '专注于电子技术、通信工程和信号处理领域的人才培养',
                'head_name': '李教授',
                'phone': '0123-45678902'
            },
            {
                'name': '机械工程学院',
                'code': 'ME',
                'description': '培养机械设计制造及其自动化、车辆工程等领域的工程技术人才',
                'head_name': '王教授',
                'phone': '0123-45678903'
            },
            {
                'name': '经济管理学院',
                'code': 'EM',
                'description': '培养经济学、管理学、金融学等领域的商业和管理人才',
                'head_name': '陈教授',
                'phone': '0123-45678904'
            },
            {
                'name': '外国语学院',
                'code': 'FL',
                'description': '培养英语、日语、法语等外国语言和跨文化交流人才',
                'head_name': '刘教授',
                'phone': '0123-45678905'
            },
            {
                'name': '物理学院',
                'code': 'PH',
                'description': '培养物理学、应用物理学等领域的科研和教学人才',
                'head_name': '赵教授',
                'phone': '0123-45678906'
            }
        ]

        departments = []
        for dept_data in departments_data:
            dept, created = Department.objects.get_or_create(
                code=dept_data['code'],
                defaults=dept_data
            )
            departments.append(dept)
            if created:
                self.stdout.write(f'创建院系: {dept.name}')
            else:
                self.stdout.write(f'院系已存在: {dept.name}')

        return departments

    def create_majors(self, departments):
        """创建专业数据"""
        majors_data = [
            # 计算机科学与技术学院的专业
            {
                'department': departments[0],  # 计算机科学与技术学院
                'name': '计算机科学与技术',
                'code': 'CS101',
                'duration': 4,
                'description': '培养具备计算机系统分析、设计、开发与应用能力的专业人才'
            },
            {
                'department': departments[0],  # 计算机科学与技术学院
                'name': '软件工程',
                'code': 'SE101',
                'duration': 4,
                'description': '培养软件系统设计、开发、测试和维护的专业技术人才'
            },
            {
                'department': departments[0],  # 计算机科学与技术学院
                'name': '人工智能',
                'code': 'AI101',
                'duration': 4,
                'description': '培养机器学习、深度学习、自然语言处理等AI技术人才'
            },

            # 电子信息工程学院的专业
            {
                'department': departments[1],  # 电子信息工程学院
                'name': '通信工程',
                'code': 'CE101',
                'duration': 4,
                'description': '培养通信系统设计、信号处理和信息传输技术人才'
            },
            {
                'department': departments[1],  # 电子信息工程学院
                'name': '电子信息工程',
                'code': 'EE101',
                'duration': 4,
                'description': '培养电子信息系统设计、开发和集成技术人才'
            },

            # 机械工程学院的专业
            {
                'department': departments[2],  # 机械工程学院
                'name': '机械设计制造及其自动化',
                'code': 'MD101',
                'duration': 4,
                'description': '培养机械设计、制造工艺和自动化技术人才'
            },
            {
                'department': departments[2],  # 机械工程学院
                'name': '车辆工程',
                'code': 'VE101',
                'duration': 4,
                'description': '培养汽车设计、制造和测试技术人才'
            },

            # 经济管理学院的专业
            {
                'department': departments[3],  # 经济管理学院
                'name': '工商管理',
                'code': 'BA101',
                'duration': 4,
                'description': '培养企业管理、市场营销、人力资源等管理人才'
            },
            {
                'department': departments[3],  # 经济管理学院
                'name': '金融学',
                'code': 'FN101',
                'duration': 4,
                'description': '培养银行、证券、保险等金融服务专业人才'
            }
        ]

        majors = []
        for major_data in majors_data:
            major, created = Major.objects.get_or_create(
                code=major_data['code'],
                defaults=major_data
            )
            majors.append(major)
            if created:
                self.stdout.write(f'创建专业: {major.name}')
            else:
                self.stdout.write(f'专业已存在: {major.name}')

        return majors

    def create_courses(self, majors):
        """创建课程数据"""
        courses_data = [
            # 计算机相关课程
            {
                'name': '数据结构与算法',
                'code': 'CS201',
                'course_type': 'required',
                'credits': 4.0,
                'hours': 64,
                'description': '学习基本数据结构和算法设计与分析'
            },
            {
                'name': '操作系统',
                'code': 'CS202',
                'course_type': 'required',
                'credits': 3.5,
                'hours': 56,
                'description': '学习操作系统的基本原理和设计方法'
            },
            {
                'name': '计算机网络',
                'code': 'CS203',
                'course_type': 'required',
                'credits': 3.0,
                'hours': 48,
                'description': '学习计算机网络协议和通信技术'
            },
            {
                'name': '数据库系统',
                'code': 'CS204',
                'course_type': 'required',
                'credits': 3.5,
                'hours': 56,
                'description': '学习数据库设计、管理和应用开发'
            },
            {
                'name': '机器学习基础',
                'code': 'AI301',
                'course_type': 'elective',
                'credits': 3.0,
                'hours': 48,
                'description': '学习机器学习的基本算法和应用'
            },
            {
                'name': '深度学习',
                'code': 'AI302',
                'course_type': 'elective',
                'credits': 3.0,
                'hours': 48,
                'description': '学习深度神经网络的设计和应用'
            },

            # 电子信息相关课程
            {
                'name': '信号与系统',
                'code': 'EE201',
                'course_type': 'required',
                'credits': 3.5,
                'hours': 56,
                'description': '学习信号与系统的基本理论和方法'
            },
            {
                'name': '数字信号处理',
                'code': 'EE202',
                'course_type': 'required',
                'credits': 3.0,
                'hours': 48,
                'description': '学习数字信号处理的基本算法和应用'
            },

            # 机械工程相关课程
            {
                'name': '理论力学',
                'code': 'ME201',
                'course_type': 'required',
                'credits': 4.0,
                'hours': 64,
                'description': '学习力学的基本理论和分析方法'
            },
            {
                'name': '材料力学',
                'code': 'ME202',
                'course_type': 'required',
                'credits': 3.5,
                'hours': 56,
                'description': '学习材料力学性能和结构分析'
            },
            {
                'name': '汽车构造',
                'code': 'VE301',
                'course_type': 'required',
                'credits': 3.0,
                'hours': 48,
                'description': '学习汽车的基本构造和工作原理'
            },

            # 管理相关课程
            {
                'name': '管理学原理',
                'code': 'BA201',
                'course_type': 'required',
                'credits': 3.0,
                'hours': 48,
                'description': '学习管理学的基本理论和方法'
            },
            {
                'name': '市场营销学',
                'code': 'BA202',
                'course_type': 'required',
                'credits': 3.0,
                'hours': 48,
                'description': '学习市场营销的基本策略和方法'
            },
            {
                'name': '投资学',
                'code': 'FN301',
                'course_type': 'elective',
                'credits': 3.0,
                'hours': 48,
                'description': '学习投资理论和投资分析方法'
            },
            {
                'name': '公司理财',
                'code': 'FN302',
                'course_type': 'required',
                'credits': 3.0,
                'hours': 48,
                'description': '学习公司财务管理和决策'
            }
        ]

        courses = []
        for course_data in courses_data:
            course, created = Course.objects.get_or_create(
                code=course_data['code'],
                defaults=course_data
            )
            courses.append(course)
            if created:
                self.stdout.write(f'创建课程: {course.name}')
            else:
                self.stdout.write(f'课程已存在: {course.name}')

        return courses