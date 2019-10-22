from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Course, Assignment, Semester, AssignmentGrade, Enrollment

# Register your models here.
admin.site.register(Course)
admin.site.register(Assignment)
admin.site.register(Semester)
admin.site.register(AssignmentGrade)
admin.site.register(Enrollment)
