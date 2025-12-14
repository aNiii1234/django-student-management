from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.decorators.cache import cache_page
from django.db.models import Count, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import CustomUserCreationForm
from .models import User
from students.models import StudentProfile, Department, Major
from django import forms

class CustomLoginView(LoginView):
    template_name = 'accounts/login_clean.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        if user.role == 'admin':
            return reverse_lazy('accounts:admin_dashboard')
        elif user.role == 'student':
            return reverse_lazy('accounts:student_dashboard')
        else:
            return reverse_lazy('students:home')

    def form_invalid(self, form):
        # 获取表单数据
        username = form.cleaned_data.get('username', '')
        password = form.cleaned_data.get('password', '')

        # 检查用户名是否存在
        if username:
            try:
                user = User.objects.get(username=username)
                # 用户名存在，检查密码是否错误
                messages.error(self.request, '密码错误，请重新输入密码！')
            except User.DoesNotExist:
                # 用户名不存在
                messages.error(self.request, '用户名不存在，请检查用户名或注册新账号！')
        else:
            # 用户名为空
            messages.error(self.request, '请输入用户名和密码！')

        return super().form_invalid(form)

class SignUpView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, '注册成功！请登录。')
        return response

def logout_view(request):
    logout(request)
    messages.info(request, '您已成功退出登录。')
    return redirect('accounts:login')

@login_required
def profile_view(request):
    user = request.user
    student_profile = None

    if user.role == 'student':
        try:
            student_profile = StudentProfile.objects.get(user=user)
        except StudentProfile.DoesNotExist:
            pass

    context = {
        'user': user,
        'student_profile': student_profile
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def edit_profile(request):
    user = request.user
    student_profile = None

    if user.role == 'student':
        try:
            student_profile = StudentProfile.objects.get(user=user)
        except StudentProfile.DoesNotExist:
            pass

    # 获取所有院系数据
    departments = Department.objects.all()

    if request.method == 'POST':
        # 更新用户基本信息
        user.email = request.POST.get('email', user.email)
        user.phone = request.POST.get('phone', user.phone)
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)

        if student_profile:
            student_profile.address = request.POST.get('address', student_profile.address)
            student_profile.emergency_contact = request.POST.get('emergency_contact', student_profile.emergency_contact)
            student_profile.emergency_phone = request.POST.get('emergency_phone', student_profile.emergency_phone)

            # 注意：院系和专业信息由管理员设置，学生无法自行修改
            # 移除了学生修改department和major的逻辑

            student_profile.save()

        user.save()
        messages.success(request, '个人资料更新成功！')
        return redirect('accounts:profile')

    context = {
        'user': user,
        'student_profile': student_profile,
        'departments': departments,
    }
    return render(request, 'accounts/edit_profile.html', context)

@login_required
@cache_page(60)  # 缓存1分钟
def admin_dashboard(request):
    if request.user.role != 'admin':
        messages.error(request, '您没有权限访问此页面！')
        return redirect('home')

    # 优化：使用单个查询获取所有统计数据
    stats = User.objects.aggregate(
        total_users=Count('id'),
        total_students=Count('id', filter=Q(role='student'))
    )
    total_student_profiles = StudentProfile.objects.count()

    # 优化：限制查询数量
    students_without_profiles = User.objects.filter(
        role='student'
    ).exclude(
        id__in=StudentProfile.objects.values_list('user_id', flat=True)
    ).order_by('-created_at')[:5]  # 只取前5个

    # 优化：减少查询时间范围和数量
    from django.utils import timezone
    from datetime import timedelta
    one_day_ago = timezone.now() - timedelta(days=1)  # 改为1天
    recent_users = User.objects.filter(
        created_at__gte=one_day_ago
    ).order_by('-created_at')[:5]  # 只取前5个

    context = {
        'total_users': stats['total_users'],
        'total_students': stats['total_students'],
        'total_student_profiles': total_student_profiles,
        'students_without_profiles': students_without_profiles,
        'students_without_profiles_count': len(students_without_profiles),
        'recent_users': recent_users,
    }
    return render(request, 'accounts/admin_dashboard.html', context)

@login_required
def student_dashboard(request):
    if request.user.role != 'student':
        messages.error(request, '您没有权限访问此页面！')
        return redirect('home')

    try:
        student_profile = StudentProfile.objects.get(user=request.user)
        enrollments = student_profile.enrollment_set.all().order_by('-academic_year', '-semester')

        # 计算平均成绩
        average_grade = None
        average_score = None
        graded_enrollments = enrollments.exclude(grade__isnull=True).exclude(grade='')

        # 统计有成绩的课程数
        total_graded_courses = graded_enrollments.count()

        if graded_enrollments.exists():
            # 计算等级制的平均GPA
            grade_points = {'A': 4.0, 'B': 3.0, 'C': 2.0, 'D': 1.0, 'F': 0.0}
            total_points = 0
            total_scores = 0
            score_count = 0

            for enrollment in graded_enrollments:
                # 等级成绩计算GPA
                if enrollment.grade in grade_points:
                    total_points += grade_points[enrollment.grade]

                # 分数成绩计算平均分
                if enrollment.score is not None:
                    total_scores += float(enrollment.score)
                    score_count += 1

            # 计算平均GPA并转换为等级
            if total_graded_courses > 0:
                average_gpa = total_points / total_graded_courses
                if average_gpa >= 3.7:
                    average_grade = 'A'
                elif average_gpa >= 2.7:
                    average_grade = 'B'
                elif average_gpa >= 1.7:
                    average_grade = 'C'
                elif average_gpa >= 1.0:
                    average_grade = 'D'
                else:
                    average_grade = 'F'

            # 计算平均分
            if score_count > 0:
                average_score = round(total_scores / score_count, 1)

        # 计算当前学期课程数
        from django.utils import timezone
        current_year = timezone.now().year
        current_month = timezone.now().month
        current_semester = '第2学期' if current_month >= 9 or current_month <= 2 else '第1学期'
        current_academic_year = f"{current_year-1}-{current_year}" if current_month <= 8 else f"{current_year}-{current_year+1}"

        current_semester_courses = enrollments.filter(
            semester=current_semester,
            academic_year=current_academic_year
        ).count()

    except StudentProfile.DoesNotExist:
        student_profile = None
        enrollments = []
        average_grade = None
        average_score = None
        total_graded_courses = 0
        current_semester_courses = 0

    context = {
        'student_profile': student_profile,
        'enrollments': enrollments,
        'average_grade': average_grade,
        'average_score': average_score,
        'total_graded_courses': total_graded_courses,
        'current_semester_courses': current_semester_courses,
    }
    return render(request, 'accounts/student_dashboard.html', context)

@login_required
def user_list(request):
    if request.user.role != 'admin':
        messages.error(request, '您没有权限访问此页面！')
        return redirect('home')

    user_type = request.GET.get('type', 'all')
    search_query = request.GET.get('search', '')
    title = '所有用户'

    # 基础查询集
    users = User.objects.all()

    # 按用户类型过滤
    if user_type == 'students':
        users = users.filter(role='student')
        title = '学生用户'
    elif user_type == 'admins':
        users = users.filter(role='admin')
        title = '管理员用户'
    else:
        title = '所有用户'

    # 搜索功能
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone__icontains=search_query)
        )
        title = f'搜索结果: "{search_query}"'

    # 排序：按注册时间倒序
    users = users.order_by('-created_at')

    # 分页功能
    paginator = Paginator(users, 10)  # 每页显示10条记录
    page = request.GET.get('page', 1)

    try:
        users_page = paginator.page(page)
    except PageNotAnInteger:
        users_page = paginator.page(1)
    except EmptyPage:
        users_page = paginator.page(paginator.num_pages)

    # 计算统计信息
    total_users = User.objects.count()
    total_students = User.objects.filter(role='student').count()
    total_admins = User.objects.filter(role='admin').count()

    # 为模板添加角色过滤函数
    def filter_role(user_list, role):
        return [user for user in user_list if user.role == role]

    context = {
        'users': users_page,
        'title': title,
        'user_type': user_type,
        'search_query': search_query,
        'total_users': total_users,
        'total_students': total_students,
        'total_admins': total_admins,
        'filter_role': filter_role,
        'is_paginated': paginator.num_pages > 1,
    }
    return render(request, 'accounts/user_list.html', context)

@login_required
def student_profile_list_admin(request):
    if request.user.role != 'admin':
        messages.error(request, '您没有权限访问此页面！')
        return redirect('home')

    students = StudentProfile.objects.select_related('user').all()
    context = {
        'students': students,
    }
    return render(request, 'accounts/student_profile_list_admin.html', context)

@login_required
def pending_student_profiles(request):
    if request.user.role != 'admin':
        messages.error(request, '您没有权限访问此页面！')
        return redirect('home')

    # 找出没有学生档案的学生用户
    students_without_profiles = User.objects.filter(role='student').exclude(
        id__in=StudentProfile.objects.values_list('user_id', flat=True)
    ).order_by('-created_at')

    context = {
        'students_without_profiles': students_without_profiles,
    }
    return render(request, 'accounts/pending_student_profiles.html', context)

@login_required
def quick_create_student_profile(request, user_id):
    if request.user.role != 'admin':
        messages.error(request, '您没有权限访问此页面！')
        return redirect('home')

    user = get_object_or_404(User, id=user_id, role='student')

    # 检查是否已经有档案
    try:
        StudentProfile.objects.get(user=user)
        messages.warning(request, f'{user.get_full_name() or user.username} 已经有学生档案了！')
        return redirect('accounts:pending_student_profiles')
    except StudentProfile.DoesNotExist:
        pass

    # 获取所有院系
    departments = Department.objects.all()

    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        real_name = request.POST.get('real_name')
        gender = request.POST.get('gender')
        birth_date = request.POST.get('birth_date')
        address = request.POST.get('address')
        emergency_contact = request.POST.get('emergency_contact')
        emergency_phone = request.POST.get('emergency_phone')
        department_id = request.POST.get('department')
        major_id = request.POST.get('major')

        try:
            department = Department.objects.get(id=department_id) if department_id else None
            major = Major.objects.get(id=major_id) if major_id else None

            student_profile = StudentProfile.objects.create(
                user=user,
                student_id=student_id,
                real_name=real_name,
                gender=gender,
                birth_date=birth_date if birth_date else None,
                address=address if address else '',
                emergency_contact=emergency_contact if emergency_contact else '',
                emergency_phone=emergency_phone if emergency_phone else '',
                department=department,
                major=major,
            )

            messages.success(request, f'成功为 {user.get_full_name() or user.username} 创建学生档案！')
            # 提供添加选课的快捷链接
            messages.info(request, f'您可以为该学生<a href="/students/enrollment/add/?student_id={student_profile.id}" class="alert-link">添加选课记录</a>以录入成绩。')
            return redirect('accounts:pending_student_profiles')
        except Exception as e:
            messages.error(request, f'创建学生档案时出错：{str(e)}')

    context = {
        'user': user,
        'departments': departments,
    }
    return render(request, 'accounts/quick_create_student_profile.html', context)

@login_required
def edit_user(request, user_id):
    if request.user.role != 'admin':
        messages.error(request, '您没有权限访问此页面！')
        return redirect('home')

    user_to_edit = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        # 获取表单数据
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        role = request.POST.get('role')

        # 验证用户名是否唯一
        if User.objects.exclude(id=user_id).filter(username=username).exists():
            messages.error(request, '用户名已存在！')
        else:
            # 更新用户信息
            user_to_edit.username = username
            user_to_edit.email = email
            user_to_edit.first_name = first_name
            user_to_edit.last_name = last_name
            user_to_edit.phone = phone
            user_to_edit.role = role
            user_to_edit.save()

            messages.success(request, f'用户 {user_to_edit.username} 的信息已更新！')
            return redirect('accounts:user_list')

    context = {
        'user_to_edit': user_to_edit,
    }
    return render(request, 'accounts/edit_user.html', context)

@login_required
def delete_user(request, user_id):
    if request.user.role != 'admin':
        messages.error(request, '您没有权限删除用户！')
        return redirect('home')

    user_to_delete = get_object_or_404(User, id=user_id)

    # 防止删除自己
    if user_to_delete == request.user:
        messages.error(request, '不能删除自己的账户！')
        return redirect('accounts:user_list')

    # 防止删除超级管理员
    if user_to_delete.is_superuser:
        messages.error(request, '不能删除超级管理员账户！')
        return redirect('accounts:user_list')

    if request.method == 'POST':
        username = user_to_delete.username
        user_to_delete.delete()
        messages.success(request, f'用户 {username} 已被成功删除！')
        return redirect('accounts:user_list')

    context = {
        'user_to_delete': user_to_delete,
    }
    return render(request, 'accounts/delete_user.html', context)