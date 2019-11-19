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
	path('student/transcript', GradeManagement.views.student_grades, name='student-grades'),
	path('student/course/<int:id>', GradeManagement.views.student_course_detail, name='student-course-detail'),
	path('goodbye', GradeManagement.views.goodbye, name='goodbye'),
    path('staff/home', GradeManagement.views.staff_home, name='staff-home'),
    path('staff/personal_info', GradeManagement.views.staff_personalinfo,name='staff-personal-info'),
    path('staff/personal_info/save', GradeManagement.views.staff_personalinfo_save,name='staff-personal-info-save'),
	path('staff/course/<int:id>', GradeManagement.views.staff_course_detail, name='staff-course-detail'),
	path('staff/course/<int:id>/', include([
        path('assignments/create', GradeManagement.views.staff_courses_assignment_create, name='staff-courses-assignment-create'),
		path('assignments/<int:aid>', GradeManagement.views.staff_courses_assignment_detail, name='staff-courses-assignment-detail'),
		path('assignments/<int:aid>/edit',  GradeManagement.views.staff_courses_assignment_edit, name='staff-courses-assignment-edit'),
        path('final_grades', GradeManagement.views.staff_courses_final_grades, name='staff-courses-final-grades'),
        path('final_grades/save', GradeManagement.views.staff_courses_final_grades_save, name='staff-courses-final-grades-save'),
    ])),
    path('staff/admin', GradeManagement.views.staff_administration, name='staff-admin'),
	path('staff/admin/', include([
		path('course/<int:id>/edit', GradeManagement.views.staff_administration_course_edit, name='staff-admin-course-edit')
	])),
]
