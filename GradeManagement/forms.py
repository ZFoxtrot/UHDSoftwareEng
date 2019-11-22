from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Assignment, Semester, Course


class AssignmentForm(forms.Form):
	title = forms.CharField(label='Title', max_length=256, required=True)
	due_date = forms.DateField(widget=forms.DateInput, label='Date', required=True)
	due_time = forms.TimeField(widget=forms.TimeInput, label='Time', required=True)
	description = forms.CharField(widget=forms.Textarea, required=True)

class SemesterForm(forms.ModelForm):

    class Meta:
        model = Semester
        fields = ('Title', 'StartDate', 'EndDate', 'Active')


class CourseForm(forms.Form):
	name = forms.CharField(label='Name', max_length=256, required=True, widget=forms.TextInput(attrs={
	'class': 'form-control'
	}))
	teacher = forms.ModelChoiceField(User.objects.filter(groups__name='Staff'), widget=forms.Select(attrs={
	'class': 'form-control'
	}))
	semester = forms.ModelChoiceField(Semester.objects.all(), widget=forms.Select(attrs={
	'class': 'form-control'
	}))

class EnrollmentForm(forms.Form):
	student = forms.ModelChoiceField(User.objects.filter(groups__name='Student'), required=True, widget=forms.Select(attrs={
	'class': 'form-control'
	}))
	course = forms.ModelChoiceField(Course.objects.all(), required=True, widget=forms.Select(attrs={
	'class': 'form-control'
	}))
	grade = forms.IntegerField(max_value=100, min_value=0, required=False, widget=forms.NumberInput(attrs={
	'class': 'form-control'
	}))

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
