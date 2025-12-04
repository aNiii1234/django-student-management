from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('register/', views.SignUpView.as_view(), name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),

    # 用户管理相关URL
    path('users/', views.user_list, name='user_list'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('student_profiles/', views.student_profile_list_admin, name='student_profile_list_admin'),
    path('pending_student_profiles/', views.pending_student_profiles, name='pending_student_profiles'),
    path('quick_create_profile/<int:user_id>/', views.quick_create_student_profile, name='quick_create_student_profile'),
]