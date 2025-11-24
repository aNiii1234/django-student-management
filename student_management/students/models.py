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

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户')
    student_id = models.CharField(max_length=20, unique=True, verbose_name='学号')
    real_name = models.CharField(max_length=50, verbose_name='真实姓名')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='性别')
    birth_date = models.DateField(null=True, blank=True, verbose_name='出生日期')
    address = models.TextField(blank=True, null=True, verbose_name='家庭住址')
    emergency_contact = models.CharField(max_length=50, blank=True, null=True, verbose_name='紧急联系人')
    emergency_phone = models.CharField(max_length=15, blank=True, null=True, verbose_name='紧急联系电话')

    # 新增院系和专业关联
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='所属院系')
    major = models.ForeignKey(Major, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='专业')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '学生档案'
        verbose_name_plural = '学生档案'

    def __str__(self):
        return f"{self.student_id} - {self.real_name}"

class Course(models.Model):
    COURSE_TYPE_CHOICES = [
        ('required', '必修课'),
        ('elective', '选修课'),
        ('practical', '实践课'),
    ]

    name = models.CharField(max_length=100, verbose_name='课程名称')
    code = models.CharField(max_length=10, unique=True, verbose_name='课程代码')
    course_type = models.CharField(max_length=10, choices=COURSE_TYPE_CHOICES, verbose_name='课程类型')
    credits = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='学分')
    hours = models.IntegerField(verbose_name='学时')
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