from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Course, Enrollment, Assignment, AssignmentGrade, Semester
from django.http import HttpResponse

def group_required(*group_names):
	# Requires user membership in at least one of the groups passed #
	def in_groups(u):
		if u.is_authenticated:
			if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
				return True
		return False

	return user_passes_test(in_groups)

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
			if bool(user.groups.filter(name__in='Student')):
				return redirect('student-home')
			else:
				return redirect('staff-home')
		else:
			return render(request, 'GradeManagement/welcome.html', { "err" : 1})
	raise Http400("")

@group_required('Student')
def student_home(request):
	StudentEnrolledCourses = Enrollment.objects.filter(Students=request.user)
	return render(request, 'GradeManagement/student_home.html', {'courses': StudentEnrolledCourses})

@group_required('Student')
def student_course_detail(request, id):
	StudentEnrolledCourses = Enrollment.objects.filter(Students=request.user)
	CourseDetail = get_object_or_404(StudentEnrolledCourses, Course_id=id)
	CourseDetail = CourseDetail.Course
	# I legit couldn't figure out how to do this query in Django's ORM, so here it is in raw SQL form
	CourseGrades = Assignment.objects.raw('SELECT GradeManagement_assignment.id, Title, Due_date, Description, Course_id, a.Grade FROM GradeManagement_assignment LEFT JOIN (SELECT GradeManagement_assignmentgrade.GradeOfAssignment as Grade, Assignment_id FROM GradeManagement_assignmentgrade WHERE GradeManagement_assignmentgrade.UserOfAssignment_id = %s) AS a ON GradeManagement_assignment.id = a.Assignment_id WHERE Course_id = %s', [request.user.id, CourseDetail.id])
	totalPoints = 0
	totalCounts = 0
	for g in CourseGrades:
		if g.Grade is not None:
			totalPoints += g.Grade
			totalCounts += 1
	average = 0
	if totalCounts > 0:
		average = totalPoints / totalCounts
	return render(request, 'GradeManagement/student_course_detail.html', {'course': CourseDetail, 'grades': CourseGrades, 'average': average})

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
@group_required('Staff')
def staff_home(request):
	return render(request, 'GradeManagement/staff_home.html')

# STAFF COURSES FUNCTIONS
@group_required('Staff')
def staff_courses(request):
	return render(request, 'GradeManagement/staff_courses.html')

@login_required
def staff_course_detail(request):
	return render(request, 'GradeManagement/staff_course_detail.html')

@login_required
def staff_courses_assignments(request):
	return render(request, 'GradeManagement/staff_courses_assignments.html')

@login_required
def staff_courses_assignments_detail(request):
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
