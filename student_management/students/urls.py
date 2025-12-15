from django.urls import path
from . import views
from . import views_api

app_name = 'students'

urlpatterns = [
    # 主页
    path('', views.home, name='home'),

    # Department URLs
    path('departments/', views.DepartmentListView.as_view(), name='department_list'),
    path('departments/create/', views.DepartmentCreateView.as_view(), name='department_create'),
    path('departments/<int:pk>/update/', views.DepartmentUpdateView.as_view(), name='department_update'),
    path('departments/<int:pk>/delete/', views.DepartmentDeleteView.as_view(), name='department_delete'),

    # Major URLs
    path('majors/', views.MajorListView.as_view(), name='major_list'),
    path('majors/create/', views.MajorCreateView.as_view(), name='major_create'),
    path('majors/<int:pk>/update/', views.MajorUpdateView.as_view(), name='major_update'),
    path('majors/<int:pk>/delete/', views.MajorDeleteView.as_view(), name='major_delete'),

    # Course URLs
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('courses/create/', views.CourseCreateView.as_view(), name='course_create'),
    path('courses/<int:pk>/update/', views.CourseUpdateView.as_view(), name='course_update'),
    path('courses/<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),

    # StudentProfile URLs
    path('students/', views.student_profile_list, name='student_profile_list'),
    path('students/create/', views.student_profile_create, name='student_profile_create'),
    path('students/<int:pk>/update/', views.student_profile_update, name='student_profile_update'),
    path('students/<int:pk>/delete/', views.student_profile_delete, name='student_profile_delete'),

    # Enrollment URLs
    path('enrollments/', views.EnrollmentListView.as_view(), name='enrollment_list'),
    path('enrollments/create/', views.EnrollmentCreateView.as_view(), name='enrollment_create'),
    path('enrollments/<int:pk>/update/', views.EnrollmentUpdateView.as_view(), name='enrollment_update'),
    path('enrollments/<int:pk>/delete/', views.EnrollmentDeleteView.as_view(), name='enrollment_delete'),

    # Grade Management URLs
    path('grades/', views.enrollment_grade_list, name='enrollment_grade_list'),
    path('grades/<int:pk>/update/', views.grade_update, name='grade_update'),

    # Student specific URLs
    path('my-enrollments/', views.my_enrollments, name='my_enrollments'),
    path('course-selection/', views.course_selection, name='course_selection'),
    path('course-selection/submit/', views.course_selection_submit, name='course_selection_submit'),

    # 导出功能
    path('export/csv/', views.export_students_csv, name='export_students_csv'),
    path('export/excel/', views.export_students_excel, name='export_students_excel'),

    # API 端点
    path('api/student-status/', views_api.api_student_status, name='api_student_status'),
    path('api/course-updates/', views_api.api_course_updates, name='api_course_updates'),
    path('api/enrollment-changes/', views_api.api_enrollment_changes, name='api_enrollment_changes'),
]