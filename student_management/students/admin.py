from django.contrib import admin
from .models import StudentProfile, Department, Major, Course, Enrollment

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'real_name', 'gender', 'user', 'created_at')
    list_filter = ('gender', 'created_at')
    search_fields = ('student_id', 'real_name', 'user__username')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'head_name', 'phone', 'created_at')
    search_fields = ('name', 'code', 'head_name')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Major)
class MajorAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'department', 'duration', 'created_at')
    list_filter = ('department', 'duration')
    search_fields = ('name', 'code', 'department__name')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'course_type', 'credits', 'hours', 'created_at')
    list_filter = ('course_type', 'credits')
    search_fields = ('name', 'code')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'major', 'semester', 'academic_year', 'grade', 'score')
    list_filter = ('semester', 'academic_year', 'grade')
    search_fields = ('student__real_name', 'course__name', 'major__name')
    readonly_fields = ('created_at', 'updated_at')