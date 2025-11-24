from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', '管理员'),
        ('student', '学生'),
        ('teacher', '教师'),
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