from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import StudentProfile, Department, Major, Course, Enrollment
from .forms import StudentProfileForm, DepartmentForm, MajorForm, CourseForm, EnrollmentForm, AdminEnrollmentForm, GradeForm

User = get_user_model()

# 权限检查混入类
class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'admin'

class StudentOrAdminMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role in ['admin', 'student']

# 主页视图（公开访问）
def home(request):
    if request.user.is_authenticated:
        if request.user.role == 'admin':
            return redirect('accounts:admin_dashboard')
        elif request.user.role == 'student':
            return redirect('accounts:student_dashboard')
        else:
            return render(request, 'students/home_clean.html')
    else:
        return render(request, 'students/home_clean.html')

# Department CRUD操作
class DepartmentListView(ListView):
    model = Department
    template_name = 'students/department_list_clean.html'
    context_object_name = 'departments'

class DepartmentCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'students/department_form.html'
    success_url = reverse_lazy('students:department_list')

class DepartmentUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'students/department_form.html'
    success_url = reverse_lazy('students:department_list')

class DepartmentDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Department
    template_name = 'students/department_confirm_delete.html'
    success_url = reverse_lazy('students:department_list')

# Major CRUD操作
class MajorListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Major
    template_name = 'students/major_list.html'
    context_object_name = 'majors'

class MajorCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Major
    form_class = MajorForm
    template_name = 'students/major_form.html'
    success_url = reverse_lazy('students:major_list')

class MajorUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Major
    form_class = MajorForm
    template_name = 'students/major_form.html'
    success_url = reverse_lazy('students:major_list')

class MajorDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Major
    template_name = 'students/major_confirm_delete.html'
    success_url = reverse_lazy('students:major_list')

# Course CRUD操作
class CourseListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Course
    template_name = 'students/course_list.html'
    context_object_name = 'courses'

class CourseCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'students/course_form.html'
    success_url = reverse_lazy('students:course_list')

class CourseUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'students/course_form.html'
    success_url = reverse_lazy('students:course_list')

class CourseDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Course
    template_name = 'students/course_confirm_delete.html'
    success_url = reverse_lazy('students:course_list')

# StudentProfile CRUD操作
@login_required
def student_profile_list(request):
    if request.user.role != 'admin':
        messages.error(request, '您没有权限访问此页面！')
        return redirect('home')

    # 获取查询参数
    search_query = request.GET.get('search', '').strip()
    department_id = request.GET.get('department', '')
    status = request.GET.get('status', '')
    gender = request.GET.get('gender', '')

    # 构建查询
    students = StudentProfile.objects.all().select_related('user', 'department', 'major')

    # 搜索功能
    if search_query:
        students = students.filter(
            Q(student_id__icontains=search_query) |
            Q(real_name__icontains=search_query) |
            Q(class_name__icontains=search_query) |
            Q(user__username__icontains=search_query)
        )

    # 院系筛选
    if department_id:
        students = students.filter(department_id=department_id)

    # 学籍状态筛选
    if status:
        students = students.filter(enrollment_status=status)

    # 性别筛选
    if gender:
        students = students.filter(gender=gender)

    # 排序
    students = students.order_by('-created_at')

    # 分页
    paginator = Paginator(students, 20)  # 每页显示20条
    page = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    # 获取所有院系用于筛选
    departments = Department.objects.all()

    context = {
        'students': page_obj,
        'departments': departments,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        # 统计数据
        'total_students': StudentProfile.objects.count(),
        'enrolled_students': StudentProfile.objects.filter(enrollment_status='enrolled').count(),
        'total_departments': Department.objects.count(),
        'total_majors': Major.objects.count(),
    }

    return render(request, 'students/student_profile_list_clean.html', context)

@login_required
def student_profile_create(request):
    if request.user.role != 'admin':
        messages.error(request, '您没有权限访问此页面！')
        return redirect('home')

    if request.method == 'POST':
        form = StudentProfileForm(request.POST)
        if form.is_valid():
            student_profile = form.save(commit=False)
            # 创建或关联用户
            username = form.cleaned_data['student_id']
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # 如果用户不存在，创建新用户
                user = User.objects.create_user(
                    username=username,
                    email=f"{username}@example.com",
                    password='123456',  # 默认密码
                    first_name=form.cleaned_data['real_name'][:1],
                    last_name=form.cleaned_data['real_name'][1:],
                    role='student'
                )
            student_profile.user = user
            student_profile.save()
            messages.success(request, '学生档案创建成功！')
            return redirect('students:student_profile_list')
    else:
        form = StudentProfileForm()

    departments = Department.objects.all()
    return render(request, 'students/student_profile_form.html', {
        'form': form,
        'departments': departments
    })

@login_required
def student_profile_update(request, pk):
    if request.user.role != 'admin':
        messages.error(request, '您没有权限访问此页面！')
        return redirect('home')

    student_profile = get_object_or_404(StudentProfile, pk=pk)

    if request.method == 'POST':
        form = StudentProfileForm(request.POST, instance=student_profile)
        if form.is_valid():
            form.save()
            messages.success(request, '学生档案更新成功！')
            return redirect('students:student_profile_list')
    else:
        form = StudentProfileForm(instance=student_profile)

    departments = Department.objects.all()
    return render(request, 'students/student_profile_form.html', {
        'form': form,
        'departments': departments
    })

@login_required
def student_profile_delete(request, pk):
    if request.user.role != 'admin':
        messages.error(request, '您没有权限访问此页面！')
        return redirect('home')

    student_profile = get_object_or_404(StudentProfile, pk=pk)

    if request.method == 'POST':
        user = student_profile.user
        student_profile.delete()
        user.delete()
        messages.success(request, '学生档案删除成功！')
        return redirect('students:student_profile_list')

    return render(request, 'students/student_profile_confirm_delete.html', {'student_profile': student_profile})

# Enrollment CRUD操作
class EnrollmentListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Enrollment
    template_name = 'students/enrollment_list.html'
    context_object_name = 'enrollments'

class EnrollmentCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Enrollment
    form_class = AdminEnrollmentForm
    template_name = 'students/enrollment_form.html'
    success_url = reverse_lazy('students:enrollment_list')

class EnrollmentUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Enrollment
    form_class = AdminEnrollmentForm
    template_name = 'students/enrollment_form.html'
    success_url = reverse_lazy('students:enrollment_list')

class EnrollmentDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Enrollment
    template_name = 'students/enrollment_confirm_delete.html'
    success_url = reverse_lazy('students:enrollment_list')

# 成绩录入和管理
@login_required
def enrollment_grade_list(request):
    if request.user.role != 'admin':
        messages.error(request, '您没有权限访问此页面！')
        return redirect('home')

    enrollments = Enrollment.objects.all().select_related('student', 'course')
    return render(request, 'students/enrollment_grade_list.html', {'enrollments': enrollments})

@login_required
def grade_update(request, pk):
    if request.user.role != 'admin':
        messages.error(request, '您没有权限访问此页面！')
        return redirect('home')

    enrollment = get_object_or_404(Enrollment, pk=pk)

    if request.method == 'POST':
        form = GradeForm(request.POST, instance=enrollment)
        if form.is_valid():
            form.save()
            messages.success(request, '成绩更新成功！')
            return redirect('students:enrollment_grade_list')
    else:
        form = GradeForm(instance=enrollment)

    return render(request, 'students/grade_form.html', {'form': form, 'enrollment': enrollment})

# 学生查看自己的选课和成绩
@login_required
def my_enrollments(request):
    if request.user.role != 'student':
        messages.error(request, '您没有权限访问此页面！')
        return redirect('home')

    try:
        student_profile = StudentProfile.objects.get(user=request.user)
        enrollments = Enrollment.objects.filter(student=student_profile).select_related('course', 'major')
        return render(request, 'students/my_enrollments.html', {'enrollments': enrollments})
    except StudentProfile.DoesNotExist:
        messages.error(request, '您还没有学生档案！')
        return redirect('home')

# 学生课程选择功能
@login_required
def course_selection(request):
    if request.user.role != 'student':
        messages.error(request, '您没有权限访问此页面！')
        return redirect('home')

    try:
        student_profile = StudentProfile.objects.get(user=request.user)

        # 获取学生已选择的课程
        enrolled_courses = Enrollment.objects.filter(
            student=student_profile
        ).values_list('course_id', flat=True)

        # 获取所有可选课程（排除已选的）
        available_courses = Course.objects.exclude(
            id__in=enrolled_courses
        ).order_by('course_type', 'name')

        # 创建选课表单实例，用于获取学期和学年选项
        enrollment_form = EnrollmentForm()

        context = {
            'available_courses': available_courses,
            'student_profile': student_profile,
            'form': enrollment_form
        }

        return render(request, 'students/course_selection.html', context)

    except StudentProfile.DoesNotExist:
        messages.error(request, '您还没有学生档案！')
        return redirect('home')

@login_required
def course_selection_submit(request):
    if request.user.role != 'student':
        messages.error(request, '您没有权限进行此操作！')
        return redirect('home')

    if request.method != 'POST':
        messages.error(request, '请求方式错误！')
        return redirect('students:course_selection')

    try:
        student_profile = StudentProfile.objects.get(user=request.user)
        course_id = request.POST.get('course')
        semester = request.POST.get('semester')
        academic_year = request.POST.get('academic_year')

        if not all([course_id, semester, academic_year]):
            messages.error(request, '请填写完整的选课信息！')
            return redirect('students:course_selection')

        # 获取课程
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            messages.error(request, '所选课程不存在！')
            return redirect('students:course_selection')

        # 检查学生是否有专业
        if not student_profile.major:
            messages.error(request, '您还没有设置专业信息，请联系管理员设置专业后再进行选课！')
            return redirect('students:course_selection')

        # 检查是否已选过该课程
        if Enrollment.objects.filter(student=student_profile, course=course).exists():
            messages.error(request, '您已经选择了该课程！')
            return redirect('students:course_selection')

        # 创建选课记录
        enrollment = Enrollment.objects.create(
            student=student_profile,
            course=course,
            major=student_profile.major,
            semester=semester,
            academic_year=academic_year
        )

        messages.success(request, f'成功选择课程：{course.name}！')
        return redirect('students:my_enrollments')

    except StudentProfile.DoesNotExist:
        messages.error(request, '您还没有学生档案！')
        return redirect('home')
    except Exception as e:
        messages.error(request, f'选课失败：{str(e)}')
        return redirect('students:course_selection')