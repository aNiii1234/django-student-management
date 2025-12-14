from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', '管理员'),
        ('student', '学生'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student', verbose_name='角色')
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name='手机号')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return self.username

@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    """
    当创建学生用户时，自动创建对应的StudentProfile
    """
    if created and instance.role == 'student':
        from students.models import StudentProfile
        # 检查是否已经存在StudentProfile（避免重复创建）
        if not StudentProfile.objects.filter(user=instance).exists():
            # 生成学号：使用STU + 年份 + 用户ID（补零到4位）
            from datetime import datetime
            year_suffix = datetime.now().year % 100
            student_id = f"STU{year_suffix}{instance.id:04d}"

            # 创建基础的学生档案
            StudentProfile.objects.create(
                user=instance,
                student_id=student_id,
                real_name=f"{instance.last_name}{instance.first_name}" if instance.first_name and instance.last_name else instance.username,
                gender='M',  # 默认值，用户后续可以修改
                phone=instance.phone,
                email=instance.email,
                enrollment_date=datetime.now().date(),  # 入学日期设为当前日期
            )

@receiver(post_save, sender=User)
def save_student_profile(sender, instance, **kwargs):
    """
    保存用户时，同步更新StudentProfile的联系信息
    """
    if instance.role == 'student':
        from students.models import StudentProfile
        try:
            student_profile = StudentProfile.objects.get(user=instance)
            # 同步基本信息
            student_profile.phone = instance.phone
            student_profile.email = instance.email
            student_profile.real_name = f"{instance.last_name}{instance.first_name}" if instance.first_name and instance.last_name else instance.username
            student_profile.save()
        except StudentProfile.DoesNotExist:
            # 如果不存在档案，则创建一个
            pass  # create_student_profile 会处理创建逻辑