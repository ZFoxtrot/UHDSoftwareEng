from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def welcome(request):
	if request.user.is_authenticated:
		return redirect('student-home')
	elif request.method == 'GET':
		return render(request, 'GradeManagement/welcome.html')
	elif request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('student-home')
		else:
			return render(request, 'GradeManagement/welcome.html', { "err" : 1})
	raise Http400("")

@login_required
def student_home(request):
	return render(request, 'GradeManagement/student_home.html')

@login_required
def student_personal_info(request):
	pass

@login_required
def student_grades(request):
	pass

def goodbye(request):
	logout(request)
	return redirect('welcome')
