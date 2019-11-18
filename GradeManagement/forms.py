from django import forms

from .models import Assignment, Semester, Course


class AssignmentForm(forms.ModelForm):

    class Meta:
        model = Assignment
        fields = ('Title', 'Due_date', 'Description', 'Course',)


class SemesterForm(forms.ModelForm):

    class Meta:
        model = Semester
        fields = ('Title', 'StartDate', 'EndDate', 'Active')


class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = ('Name', 'Teacher', 'SemesterOfCourse')
