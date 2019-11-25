from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Assignment, Semester, Course


class AssignmentForm(forms.Form):
	title = forms.CharField(label='Title', max_length=256, required=True)
	due_date = forms.DateField(widget=forms.DateInput, label='Date', required=True)
	due_time = forms.TimeField(widget=forms.TimeInput, label='Time', required=True)
	description = forms.CharField(widget=forms.Textarea, required=True)

class SemesterForm(forms.Form):
	title = forms.CharField(label='Title', max_length=256, required=True, widget=forms.TextInput(attrs={
	'class': 'form-control'
	}))
	start_date = forms.DateField(label='Start Date', required=True, widget=forms.DateInput(attrs={
	'class': 'form-control'
	}))
	end_date = forms.DateField(label='End Date', required=True, widget=forms.DateInput(attrs={
	'class': 'form-control'
	}))
	active = forms.BooleanField(label='Active', required=False, widget=forms.CheckboxInput(attrs={
	'class': 'form-control'
	}))


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


class AddUserForm(forms.Form):
	username = forms.CharField(label='Username', max_length=256, required=True, widget=forms.TextInput(attrs={
	'class': 'form-control'
	}))
	firstname = forms.CharField(label='FirstName', max_length=256, required=True, widget=forms.TextInput(attrs={
	'class': 'form-control'
	}))
	lastname = forms.CharField(label='LastName', max_length=256, required=True, widget=forms.TextInput(attrs={
	'class': 'form-control'
	}))
	email = forms.CharField(label='Email', max_length=256, required=True, widget=forms.EmailInput(attrs={
	'class': 'form-control'
	}))
	Group = forms.ModelChoiceField(Group.objects.all(), required=True, widget=forms.Select(attrs={
	'class': 'form-control'
	}))
	password = forms.CharField(label='Password', max_length=256, required=True, widget=forms.PasswordInput(attrs={
	'class': 'form-control'
	}))

class EditUserForm(forms.Form):
	username = forms.CharField(label='Username', max_length=256, required=True, widget=forms.TextInput(attrs={
	'class': 'form-control'
	}))
	firstname = forms.CharField(label='FirstName', max_length=256, required=True, widget=forms.TextInput(attrs={
	'class': 'form-control'
	}))
	lastname = forms.CharField(label='LastName', max_length=256, required=True, widget=forms.TextInput(attrs={
	'class': 'form-control'
	}))
	email = forms.CharField(label='Email', max_length=256, required=True, widget=forms.EmailInput(attrs={
	'class': 'form-control'
	}))
	Group = forms.ModelChoiceField(Group.objects.all(), required=True, widget=forms.Select(attrs={
	'class': 'form-control'
	}))
