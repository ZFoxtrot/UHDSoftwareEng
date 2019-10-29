"""UHDSoftwareEng URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
import GradeManagement.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', GradeManagement.views.welcome, name='welcome'),  # Home page will redirect to views.home in LoginPage
	path('student/home', GradeManagement.views.student_home, name='student-home'),
	path('student/personal_info', GradeManagement.views.student_personal_info, name='student-personal-info'),
	path('student/grades', GradeManagement.views.student_grades, name='student-grades'),
	path('goodbye', GradeManagement.views.goodbye, name='goodbye'),
    path('staff/home', GradeManagement.views.staff_home, name='staff-home'),
    path('staff/personal_info', GradeManagement.views.staff_personalinfo,name='staff-personal-info'),
    path('staff/courses', GradeManagement.views.staff_courses, name='staff-courses'),
	path('staff/courses/<int:id>', GradeManagement.views.staff_course_detail, name='staff-course-detail'),
	path('staff/courses/<int:id>/', include([
        path('assignments', GradeManagement.views.staff_courses_assignments, name='staff-courses-assignments'),
		path('assignments/<int:id>', GradeManagement.views.staff_courses_assignments_detail, name='staff-courses-assignments-detail'),
		path('assignments/<int:id>/', include([
            path('edit', GradeManagement.views.staff_courses_assignments_edit, name='staff-courses-assignments-edit'),
            path('modify', GradeManagement.views.staff_courses_assigments_modify, name='staff-courses-assignments-modify'),
            path('create', GradeManagement.views.staff_courses_assignments_create, name='staff-courses-assignments-create'),
        ])),
        path('students', GradeManagement.views.staff_courses_students, name='staff-courses-students'),
		path('students/<int:id>/final_grade', GradeManagement.views.staff_course_students_setFinalGrade, name='staff-courses-final-grade'),
    ])),
    path('staff/admin', GradeManagement.views.staff_administration, name='staff-admin'),
]
