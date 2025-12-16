from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='院系名称')
    code = models.CharField(max_length=10, unique=True, verbose_name='院系代码')
    description = models.TextField(blank=True, null=True, verbose_name='院系描述')
    head_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='院系负责人')
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name='联系电话')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '院系'
        verbose_name_plural = '院系'

    def __str__(self):
        return self.name

class Major(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='所属院系')
    name = models.CharField(max_length=100, verbose_name='专业名称')
    code = models.CharField(max_length=10, unique=True, verbose_name='专业代码')
    duration = models.IntegerField(default=4, verbose_name='学制(年)')
    description = models.TextField(blank=True, null=True, verbose_name='专业描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '专业'
        verbose_name_plural = '专业'

    def __str__(self):
        return f"{self.name} ({self.department.name})"

class StudentProfile(models.Model):
    GENDER_CHOICES = [
        ('M', '男'),
        ('F', '女'),
    ]

    POLITICAL_STATUS_CHOICES = [
        ('', '请选择'),
        ('member', '党员'),
        ('probationary_member', '预备党员'),
        ('league_member', '团员'),
        ('masses', '群众'),
    ]

    ENROLLMENT_STATUS_CHOICES = [
        ('enrolled', '在读'),
        ('suspended', '休学'),
        ('graduated', '已毕业'),
        ('dropped_out', '退学'),
        ('transferred', '转出'),
    ]

    # 学期和学年选择常量
    SEMESTER_CHOICES = [
        ('1', '第1学期（大一上）'),
        ('2', '第2学期（大一下）'),
        ('3', '第3学期（大二上）'),
        ('4', '第4学期（大二下）'),
        ('5', '第5学期（大三上）'),
        ('6', '第6学期（大三下）'),
        ('7', '第7学期（大四上）'),
        ('8', '第8学期（大四下）'),
    ]

    ACADEMIC_YEAR_CHOICES = [
        ('2020-2021', '2020-2021学年'),
        ('2021-2022', '2021-2022学年'),
        ('2022-2023', '2022-2023学年'),
        ('2023-2024', '2023-2024学年'),
        ('2024-2025', '2024-2025学年'),
        ('2025-2026', '2025-2026学年'),
        ('2026-2027', '2026-2027学年'),
        ('2027-2028', '2027-2028学年'),
        ('2028-2029', '2028-2029学年'),
        ('2029-2030', '2029-2030学年'),
        ('2030-2031', '2030-2031学年'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户')
    student_id = models.CharField(max_length=20, unique=True, verbose_name='学号')
    real_name = models.CharField(max_length=50, verbose_name='真实姓名')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='性别')
    birth_date = models.DateField(null=True, blank=True, verbose_name='出生日期')

    # 身份证件信息
    id_card_number = models.CharField(max_length=18, blank=True, null=True, unique=True, verbose_name='身份证号')
    nationality = models.CharField(max_length=20, default='汉族', verbose_name='民族')

    # 联系方式
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name='手机号码')
    email = models.EmailField(blank=True, null=True, verbose_name='个人邮箱')
    address = models.TextField(blank=True, null=True, verbose_name='家庭住址')

    # 学籍信息
    enrollment_date = models.DateField(null=True, blank=True, verbose_name='入学日期')
    graduation_date = models.DateField(null=True, blank=True, verbose_name='预计毕业日期')
    enrollment_status = models.CharField(max_length=20, choices=ENROLLMENT_STATUS_CHOICES, default='enrolled', verbose_name='学籍状态')

    # 政治面貌
    political_status = models.CharField(max_length=20, choices=POLITICAL_STATUS_CHOICES, blank=True, null=True, verbose_name='政治面貌')

    # 紧急联系人
    emergency_contact = models.CharField(max_length=50, blank=True, null=True, verbose_name='紧急联系人1')
    emergency_phone = models.CharField(max_length=15, blank=True, null=True, verbose_name='紧急联系电话1')
    emergency_relation = models.CharField(max_length=20, blank=True, null=True, verbose_name='与学生关系1')

    # 第二位紧急联系人
    emergency_contact2 = models.CharField(max_length=50, blank=True, null=True, verbose_name='紧急联系人2')
    emergency_phone2 = models.CharField(max_length=15, blank=True, null=True, verbose_name='紧急联系电话2')
    emergency_relation2 = models.CharField(max_length=20, blank=True, null=True, verbose_name='与学生关系2')

    # 新增院系和专业关联
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='所属院系')
    major = models.ForeignKey(Major, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='专业')

    # 当前学业状态
    current_semester = models.CharField(max_length=2, blank=True, null=True, choices=SEMESTER_CHOICES, verbose_name='当前学期')
    current_academic_year = models.CharField(max_length=10, blank=True, null=True, choices=ACADEMIC_YEAR_CHOICES, verbose_name='当前学年')
    grade_level = models.CharField(max_length=10, blank=True, null=True, choices=[
        ('1', '大一'),
        ('2', '大二'),
        ('3', '大三'),
        ('4', '大四'),
        ('graduate', '研究生'),
    ], verbose_name='年级')

    # 个人描述
    bio = models.TextField(blank=True, null=True, verbose_name='个人简介')
    hobbies = models.CharField(max_length=500, blank=True, null=True, verbose_name='兴趣爱好')
    skills = models.CharField(max_length=500, blank=True, null=True, verbose_name='特长技能')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '学生档案'
        verbose_name_plural = '学生档案'

    def __str__(self):
        return f"{self.student_id} - {self.real_name}"

    @property
    def age(self):
        """计算年龄"""
        from datetime import date
        if self.birth_date:
            today = date.today()
            return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return None

class Course(models.Model):
    COURSE_TYPE_CHOICES = [
        ('required', '必修课'),
        ('elective', '选修课'),
        ('practical', '实践课'),
    ]

    # 引用StudentProfile中定义的常量
    SEMESTER_CHOICES = StudentProfile.SEMESTER_CHOICES
    ACADEMIC_YEAR_CHOICES = StudentProfile.ACADEMIC_YEAR_CHOICES

    name = models.CharField(max_length=100, verbose_name='课程名称')
    code = models.CharField(max_length=10, unique=True, verbose_name='课程代码')
    course_type = models.CharField(max_length=10, choices=COURSE_TYPE_CHOICES, verbose_name='课程类型')
    credits = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='学分')
    hours = models.IntegerField(verbose_name='学时')
    semester = models.CharField(max_length=2, default='1', choices=SEMESTER_CHOICES, verbose_name='开设学期')
    academic_year = models.CharField(max_length=10, default='2024-2025', choices=ACADEMIC_YEAR_CHOICES, verbose_name='学年')
    description = models.TextField(blank=True, null=True, verbose_name='课程描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = '课程'

    def __str__(self):
        return self.name

class Enrollment(models.Model):
    GRADE_CHOICES = [
        ('A', '优秀 (90-100)'),
        ('B', '良好 (80-89)'),
        ('C', '中等 (70-79)'),
        ('D', '及格 (60-69)'),
        ('F', '不及格 (<60)'),
    ]

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, verbose_name='学生')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程')
    major = models.ForeignKey(Major, on_delete=models.CASCADE, verbose_name='专业')
    enrollment_date = models.DateField(auto_now_add=True, verbose_name='选课时间')
    grade = models.CharField(max_length=1, choices=GRADE_CHOICES, blank=True, null=True, verbose_name='成绩等级')
    score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='分数')
    semester = models.CharField(max_length=20, verbose_name='学期')
    academic_year = models.CharField(max_length=10, verbose_name='学年')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '选课记录'
        verbose_name_plural = '选课记录'
        unique_together = ['student', 'course', 'semester']

    def __str__(self):
        return f"{self.student.real_name} - {self.course.name} ({self.semester})"