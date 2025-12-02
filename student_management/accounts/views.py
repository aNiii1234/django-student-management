from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from .forms import CustomUserCreationForm
from .models import User
from students.models import StudentProfile, Department, Major

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

            # 更新院系和专业信息
            department_id = request.POST.get('department')
            major_id = request.POST.get('major')

            if department_id:
                try:
                    student_profile.department = Department.objects.get(id=department_id)
                except Department.DoesNotExist:
                    student_profile.department = None
            else:
                student_profile.department = None

            if major_id:
                try:
                    student_profile.major = Major.objects.get(id=major_id)
                except Major.DoesNotExist:
                    student_profile.major = None
            else:
                student_profile.major = None

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
def admin_dashboard(request):
    if request.user.role != 'admin':
        messages.error(request, '您没有权限访问此页面！')
        return redirect('home')

    # 统计数据
    total_users = User.objects.count()
    total_students = User.objects.filter(role='student').count()
    total_teachers = User.objects.filter(role='teacher').count()
    total_student_profiles = StudentProfile.objects.count()

    # 找出没有学生档案的学生用户
    students_without_profiles = User.objects.filter(role='student').exclude(
        id__in=StudentProfile.objects.values_list('user_id', flat=True)
    ).order_by('-created_at')

    # 找出最近3天内注册的新用户
    from django.utils import timezone
    from datetime import timedelta
    three_days_ago = timezone.now() - timedelta(days=3)
    recent_users = User.objects.filter(created_at__gte=three_days_ago).order_by('-created_at')

    context = {
        'total_users': total_users,
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_student_profiles': total_student_profiles,
        'students_without_profiles': students_without_profiles,
        'students_without_profiles_count': students_without_profiles.count(),
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
    except StudentProfile.DoesNotExist:
        student_profile = None
        enrollments = []

    context = {
        'student_profile': student_profile,
        'enrollments': enrollments,
    }
    return render(request, 'accounts/student_dashboard.html', context)

@login_required
def user_list(request):
    if request.user.role != 'admin':
        messages.error(request, '您没有权限访问此页面！')
        return redirect('home')

    user_type = request.GET.get('type', 'all')
    title = '所有用户'

    if user_type == 'students':
        users = User.objects.filter(role='student')
        title = '学生用户'
    elif user_type == 'teachers':
        users = User.objects.filter(role='teacher')
        title = '教师用户'
    elif user_type == 'admins':
        users = User.objects.filter(role='admin')
        title = '管理员用户'
    else:
        users = User.objects.all()
        title = '所有用户'

    context = {
        'users': users,
        'title': title,
        'user_type': user_type,
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
            return redirect('accounts:pending_student_profiles')
        except Exception as e:
            messages.error(request, f'创建学生档案时出错：{str(e)}')

    context = {
        'user': user,
        'departments': departments,
    }
    return render(request, 'accounts/quick_create_student_profile.html', context)