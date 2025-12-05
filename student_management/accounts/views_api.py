from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta
from .models import User
from students.models import StudentProfile
import json

@login_required
@require_http_methods(["GET"])
def api_pending_profiles_count(request):
    """
    API: 获取待处理学生档案数量
    """
    if request.user.role != 'admin':
        return JsonResponse({'error': '无权限'}, status=403)

    # 获取缓存的上次查询时间
    cache_key = 'pending_profiles_last_check'
    last_check = cache.get(cache_key, None)

    # 查找没有学生档案的学生用户
    students_without_profiles = User.objects.filter(role='student').exclude(
        id__in=StudentProfile.objects.values_list('user_id', flat=True)
    ).order_by('-created_at')

    count = students_without_profiles.count()

    # 检查是否有新注册的学生（对比上次检查时间）
    new_students_count = 0
    if last_check:
        new_students_count = students_without_profiles.filter(
            created_at__gt=last_check
        ).count()
    else:
        # 首次检查，只显示总数
        new_students_count = count

    # 更新缓存
    cache.set(cache_key, timezone.now(), timeout=300)  # 缓存5分钟

    return JsonResponse({
        'count': count,
        'new_students': new_students_count,
        'has_updates': new_students_count > 0,
        'timestamp': timezone.now().isoformat()
    })

@login_required
@require_http_methods(["GET"])
def api_recent_users(request):
    """
    API: 获取最近用户信息和统计数据
    """
    if request.user.role != 'admin':
        return JsonResponse({'error': '无权限'}, status=403)

    cache_key = f'user_stats_{request.user.id}'
    cached_stats = cache.get(cache_key, {})

    # 获取当前统计数据
    total_users = User.objects.count()
    total_students = User.objects.filter(role='student').count()
    total_teachers = User.objects.filter(role='teacher').count()
    total_admins = User.objects.filter(role='admin').count()
    total_student_profiles = StudentProfile.objects.count()

    # 检查是否有更新
    has_updates = (
        cached_stats.get('total_users') != total_users or
        cached_stats.get('total_students') != total_students or
        cached_stats.get('total_teachers') != total_teachers or
        cached_stats.get('total_student_profiles') != total_student_profiles
    )

    # 获取最近注册的用户
    from datetime import datetime, timedelta
    three_days_ago = timezone.now() - timedelta(days=3)
    recent_users = User.objects.filter(
        created_at__gte=three_days_ago
    ).order_by('-created_at')[:5]

    recent_users_data = [{
        'id': user.id,
        'username': user.username,
        'full_name': user.get_full_name() or user.username,
        'role': user.role,
        'created_at': user.created_at.isoformat(),
        'has_profile': StudentProfile.objects.filter(user=user).exists() if user.role == 'student' else True
    } for user in recent_users]

    # 更新缓存
    cache.set(cache_key, {
        'total_users': total_users,
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_admins': total_admins,
        'total_student_profiles': total_student_profiles,
    }, timeout=300)  # 缓存5分钟

    return JsonResponse({
        'total_users': total_users,
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_admins': total_admins,
        'total_student_profiles': total_student_profiles,
        'has_updates': has_updates,
        'recent_users': recent_users_data,
        'timestamp': timezone.now().isoformat()
    })

@login_required
@require_http_methods(["GET"])
def api_student_profiles_updates(request):
    """
    API: 检查学生档案更新
    """
    if request.user.role != 'admin':
        return JsonResponse({'error': '无权限'}, status=403)

    # 获取上次检查时间（从请求头或缓存中）
    if_modified_since = request.META.get('HTTP_IF_MODIFIED_SINCE')
    cache_key = f'profiles_last_check_{request.user.id}'
    last_check = cache.get(cache_key)

    if last_check:
        check_time = last_check
    else:
        check_time = timezone.now() - timedelta(minutes=5)  # 默认检查5分钟内的更新

    # 查找最近更新的学生档案
    updated_profiles = StudentProfile.objects.filter(
        updated_at__gt=check_time
    ).select_related('user').order_by('-updated_at')[:10]

    has_updates = updated_profiles.exists()

    # 更新缓存
    cache.set(cache_key, timezone.now(), timeout=300)  # 缓存5分钟

    if has_updates:
        updated_data = [{
            'id': profile.id,
            'student_id': profile.student_id,
            'name': profile.real_name,
            'username': profile.user.username,
            'updated_at': profile.updated_at.isoformat()
        } for profile in updated_profiles]
    else:
        updated_data = []

    return JsonResponse({
        'has_updates': has_updates,
        'updated_profiles': updated_data,
        'count': len(updated_data),
        'timestamp': timezone.now().isoformat()
    })

@login_required
@require_http_methods(["GET"])
def api_user_notifications(request):
    """
    API: 获取用户通知和状态更新
    """
    notifications = []
    user = request.user

    if user.role == 'admin':
        # 管理员通知
        pending_count = User.objects.filter(role='student').exclude(
            id__in=StudentProfile.objects.values_list('user_id', flat=True)
        ).count()

        if pending_count > 0:
            notifications.append({
                'type': 'warning',
                'title': '待处理学生档案',
                'message': f'有 {pending_count} 名学生的档案需要创建',
                'action_url': '/accounts/pending_student_profiles/'
            })

        # 最近24小时的新用户
        yesterday = timezone.now() - timedelta(hours=24)
        new_users_count = User.objects.filter(
            created_at__gte=yesterday
        ).count()

        if new_users_count > 0:
            notifications.append({
                'type': 'info',
                'title': '新用户注册',
                'message': f'最近24小时有 {new_users_count} 名新用户注册',
                'action_url': '/accounts/users/'
            })

    elif user.role == 'student':
        # 学生通知
        try:
            profile = StudentProfile.objects.get(user=user)

            # 检查档案完整性
            if not profile.department or not profile.major:
                notifications.append({
                    'type': 'warning',
                    'title': '档案信息不完整',
                    'message': '请完善您的院系和专业信息',
                    'action_url': '/accounts/edit_profile/'
                })

            # 最近的选课记录
            recent_enrollments = profile.enrollment_set.filter(
                created_at__gte=timezone.now() - timedelta(days=7)
            )

            if recent_enrollments.exists():
                notifications.append({
                    'type': 'success',
                    'title': '选课成功',
                    'message': f'您最近成功选了 {recent_enrollments.count()} 门课程',
                    'action_url': '/students/my_enrollments/'
                })

        except StudentProfile.DoesNotExist:
            notifications.append({
                'type': 'error',
                'title': '缺少学生档案',
                'message': '您还没有学生档案，请联系管理员创建',
                'action_url': '/accounts/profile/'
            })

    return JsonResponse({
        'notifications': notifications,
        'count': len(notifications),
        'timestamp': timezone.now().isoformat()
    })

@login_required
@require_http_methods(["POST"])
def api_mark_notifications_read(request):
    """
    API: 标记通知为已读（可扩展功能）
    """
    # 这里可以实现更复杂的通知系统
    return JsonResponse({
        'status': 'success',
        'message': '通知已标记为已读'
    })