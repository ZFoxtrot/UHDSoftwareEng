from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

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


# Form for creating additional users
# Inherits django's user creation form
class AddUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        user = super(AddUserForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_date['last_name']
        user.email = self.cleaned_date['email']
        user.save()
        return user


class EditUserForm(UserChangeForm):

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
        )
