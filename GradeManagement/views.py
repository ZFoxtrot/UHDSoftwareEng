from django.shortcuts import render
from django.contrib.auth import authenticate, login

def login(request):
	if request.method == 'GET':
		return render(request, 'GradeManagement/login.html')
	elif request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return render(request, 'GradeManagement/dashboard.html')
		else:
			return render(request, 'GradeManagement/login.html', { "err" : "1"})
	raise Http400("")
