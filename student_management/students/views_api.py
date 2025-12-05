from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta
from .models import StudentProfile, Enrollment, Course

@login_required
@require_http_methods(["GET"])
def api_student_status(request):
    """
    API: 获取学生状态信息
    """
    user = request.user

    if user.role != 'student':
        return JsonResponse({'error': '无权限'}, status=403)

    try:
        profile = StudentProfile.objects.get(user=user)

        # 检查档案完整性
        is_profile_complete = all([
            profile.department,
            profile.major,
            profile.real_name,
            profile.phone
        ])

        profile_status = 'complete' if is_profile_complete else 'incomplete'

        # 获取最近的选课记录
        recent_enrollments = Enrollment.objects.filter(
            student=profile,
            created_at__gte=timezone.now() - timedelta(days=7)
        ).select_related('course').order_by('-created_at')[:5]

        enrollments_data = [{
            'course_name': enrollment.course.name,
            'course_code': enrollment.course.code,
            'semester': enrollment.semester,
            'academic_year': enrollment.academic_year,
            'enrolled_at': enrollment.enrollment_date.isoformat()
        } for enrollment in recent_enrollments]

        # 获取当前学期的所有选课
        current_semester = get_current_semester()
        current_enrollments = Enrollment.objects.filter(
            student=profile,
            semester=current_semester['semester'],
            academic_year=current_semester['year']
        ).select_related('course').count()

        return JsonResponse({
            'profile_status': profile_status,
            'is_complete': is_profile_complete,
            'new_enrollments': enrollments_data,
            'current_semester_courses': current_enrollments,
            'student_id': profile.student_id,
            'department': profile.department.name if profile.department else None,
            'major': profile.major.name if profile.major else None,
            'has_updates': len(enrollments_data) > 0,
            'timestamp': timezone.now().isoformat()
        })

    except StudentProfile.DoesNotExist:
        return JsonResponse({
            'profile_status': 'missing',
            'is_complete': False,
            'has_updates': True,
            'message': '您还没有学生档案，请联系管理员创建',
            'timestamp': timezone.now().isoformat()
        })

@login_required
@require_http_methods(["GET"])
def api_course_updates(request):
    """
    API: 获取课程更新信息
    """
    if request.user.role not in ['student', 'teacher']:
        return JsonResponse({'error': '无权限'}, status=403)

    cache_key = f'course_updates_{request.user.id}'
    last_check = cache.get(cache_key, timezone.now() - timedelta(hours=1))

    # 获取最近更新的课程
    updated_courses = Course.objects.filter(
        updated_at__gt=last_check
    ).order_by('-updated_at')[:10]

    has_updates = updated_courses.exists()

    courses_data = [{
        'id': course.id,
        'name': course.name,
        'code': course.code,
        'course_type': course.course_type,
        'credits': float(course.credits),
        'updated_at': course.updated_at.isoformat()
    } for course in updated_courses]

    # 更新缓存
    cache.set(cache_key, timezone.now(), timeout=3600)  # 缓存1小时

    return JsonResponse({
        'has_updates': has_updates,
        'updated_courses': courses_data,
        'count': len(courses_data),
        'timestamp': timezone.now().isoformat()
    })

@login_required
@require_http_methods(["GET"])
def api_enrollment_changes(request):
    """
    API: 获取选课变更信息
    """
    if request.user.role != 'admin':
        return JsonResponse({'error': '无权限'}, status=403)

    cache_key = 'enrollment_changes_last_check'
    last_check = cache.get(cache_key, timezone.now() - timedelta(minutes=30))

    # 获取最近的选课变更
    recent_enrollments = Enrollment.objects.filter(
        created_at__gt=last_check
    ).select_related('student__user', 'course').order_by('-created_at')[:20]

    has_updates = recent_enrollments.exists()

    enrollments_data = [{
        'id': enrollment.id,
        'student_name': enrollment.student.real_name,
        'student_username': enrollment.student.user.username,
        'course_name': enrollment.course.name,
        'course_code': enrollment.course.code,
        'semester': enrollment.semester,
        'academic_year': enrollment.academic_year,
        'enrolled_at': enrollment.enrollment_date.isoformat()
    } for enrollment in recent_enrollments]

    # 统计信息
    stats = {
        'total_today': Enrollment.objects.filter(
            enrollment_date=timezone.now().date()
        ).count(),
        'total_this_week': Enrollment.objects.filter(
            enrollment_date__gte=timezone.now() - timedelta(days=7)
        ).count(),
        'total_this_month': Enrollment.objects.filter(
            enrollment_date__gte=timezone.now() - timedelta(days=30)
        ).count()
    }

    # 更新缓存
    cache.set(cache_key, timezone.now(), timeout=1800)  # 缓存30分钟

    return JsonResponse({
        'has_updates': has_updates,
        'recent_enrollments': enrollments_data,
        'count': len(enrollments_data),
        'stats': stats,
        'timestamp': timezone.now().isoformat()
    })

def get_current_semester():
    """
    获取当前学期信息
    """
    now = timezone.now()
    year = now.year

    # 简单的学期判断逻辑（可根据实际情况调整）
    if now.month >= 2 and now.month <= 7:
        semester = '春季学期'
    elif now.month >= 8 and now.month <= 12:
        semester = '秋季学期'
    else:
        semester = '冬季学期'
        year = year - 1 if now.month == 1 else year

    return {
        'year': str(year),
        'semester': semester
    }