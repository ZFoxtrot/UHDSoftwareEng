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

######################
# START: STAFF VIEWS #
######################
@login_required
def staff_home(request):
	return render(request, 'GradeManagement/staff_home.html')

# STAFF COURSES FUNCTIONS
@login_required
def staff_courses(request):
	return render(request, 'GradeManagement/staff_courses.html')

@login_required
def staff_courses_assignments(request):
	return render(request, 'GradeManagement/staff_courses_assignments.html')

@login_required
def staff_courses_assignments_create(request):
	return render(request, 'GradeManagement/staff_courses_assignments_create.html')

@login_required
def staff_courses_assigments_modify(request):
	return render(request, 'GradeManagement/staff_courses_assigments_modify.html')

@login_required
def staff_courses_assignments_edit(request):
	return render(request, 'GradeManagement/staff_courses_assignments_edit.html')

@login_required
def staff_courses_students(request):
	return render(request, 'GradeManagement/staff_courses_students.html')

@login_required
def staff_course_students_setFinalGrade(request):
	return render(request, 'GradeManagement/staff_course_students_setFinalGrade.html')


# STAFF PERSONAL INFO FUNCTIONS
@login_required
def staff_personalinfo(request):
	return render(request, 'GradeManagement/staff_personalinfo.html')

@login_required
def staff_personalinfo_editinfo(request):
	return render(request, 'GradeManagement/staff_personalinfo_editinfo.html')

# STAFF ADMIN FUNCTIONS
@login_required
def staff_administration(request):
	return render(request, 'GradeManagement/staff_administration.html')


## STAFF ON USER FUNCTIONS
@login_required
def staff_administration_users(request):
	return render(request, 'GradeManagement/staff_administration_users.html')

@login_required
def staff_administration_users_addUser(request):
	return render(request, 'GradeManagement/staff_administration_users_addUser.html')

@login_required
def staff_administration_users_addUser_save(request):
	return render(request, 'GradeManagement/staff_administration_users_addUser_save.html')

@login_required
def staff_administration_users_details(request):
	return render(request, 'GradeManagement/staff_administration_users_details.html')

@login_required
def staff_administration_users_details_editUser(request):
	return render(request, 'GradeManagement/staff_administration_users_details_editUser.html')

@login_required
def staff_administration_users_details_deactivateUser(request):
	return render(request, 'GradeManagement/staff_administration_users_details_deactivateUser.html')


## STAFF ON COURSE FUNCTIONS
@login_required
def staff_administration_courses(request):
	return render(request, 'GradeManagement/staff_administration_courses.html')

@login_required
def staff_adminstration_courses_addcourse(request):
	return render(request, 'GradeManagement/staff_adminstration_courses_addcourse.html')

@login_required
def staff_adminstration_courses_details(request):
	return render(request, 'GradeManagement/staff_adminstration_courses_details.html')

@login_required
def staff_administration_course_duplicate(request):
	return render(request, 'GradeManagement/staff_administration_course_duplicate.html')

@login_required
def staff_administration_course_edit(request):
	return render(request, 'GradeManagement/staff_administration_course_edit.html')


## STAFF ON SEMESTER FUNCTIONS
@login_required
def staff_administration_semesters(request):
	return render(request, 'GradeManagement/staff_administration_semesters.html')

@login_required
def staff_administration_semesters_add(request):
	return render(request, 'GradeManagement/staff_administration_semesters_add.html')

@login_required
def staff_administration_semesters_setCurrent(request):
	return render(request, 'GradeManagement/staff_administration_semesters_setCurrent.html')

####################
# END: STAFF VIEWS #
####################
