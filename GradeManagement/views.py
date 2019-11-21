from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Course, Enrollment, Assignment, AssignmentGrade, Semester
from django.http import HttpResponse, JsonResponse
from .forms import AssignmentForm, SemesterForm, CourseForm

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
		if request.user.groups.filter(name="Student").exists():
			return redirect('student-home')
		else:
			return redirect('staff-home')
	elif request.method == 'GET':
		return render(request, 'GradeManagement/welcome.html')
	elif request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			if request.user.groups.filter(name="Student").exists():
				return redirect('student-home')
			else:
				return redirect('staff-home')
		else:
			return render(request, 'GradeManagement/welcome.html', { "err" : 1})
	raise Http400("")

@group_required('Student')
def student_home(request):
	StudentEnrolledCourses = Enrollment.objects.filter(Students=request.user, Course__SemesterOfCourse__Active=True)
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

@group_required('Student')
def student_personal_info(request):
	return render(request, 'GradeManagement/student_personal_info.html')

@group_required('Student')
def student_grades(request):
	SortedEnrollments = request.user.enrollment_set.all().order_by('Course__SemesterOfCourse__StartDate')
	SemesterSorts = []
	CurrentDictionary = {
		"Semester": SortedEnrollments[0].Course.SemesterOfCourse,
		"Enrollments": [],
		"TotalPoints": 0,
		"TotalClasses": 0,
		"Average": 0
	}
	CareerTotalPoints = 0
	CareerTotalClasses = 0
	CareerTotalAverage = 0
	for e in SortedEnrollments:
		if e.Course.SemesterOfCourse != CurrentDictionary["Semester"]:
			SemesterSorts.append(CurrentDictionary)
			CurrentDictionary = {
				"Semester": e.Course.SemesterOfCourse,
				"Enrollments": [],
				"TotalPoints": 0,
				"TotalClasses": 0,
				"Average": 0
			}
		if e.Grade >= 0:
			CareerTotalPoints += e.Grade
			CurrentDictionary["TotalPoints"] += e.Grade
			CareerTotalClasses += 1
			CurrentDictionary["TotalClasses"] += 1
			CurrentDictionary["Average"] = CurrentDictionary["TotalPoints"] / CurrentDictionary["TotalClasses"]
		CurrentDictionary["Enrollments"].append(e)
	SemesterSorts.append(CurrentDictionary)
	CareerTotalAverage = CareerTotalPoints / CareerTotalClasses
	return render(request, 'GradeManagement/student_transcript.html', {'transcript': SemesterSorts, 'average': CareerTotalAverage})

def goodbye(request):
	logout(request)
	return redirect('welcome')

######################
# START: STAFF VIEWS #
######################
@group_required('Staff')
def staff_home(request):
	StaffCourses = Course.objects.filter(Teacher = request.user, SemesterOfCourse__Active = True)
	return render(request, 'GradeManagement/staff_home.html', {'courses': StaffCourses})

# STAFF PERSONAL INFO FUNCTIONS
@group_required('Staff')
def staff_personalinfo(request):
	AllGroups = Group.objects.all()
	return render(request, 'GradeManagement/staff_personal_info.html', {'groups': AllGroups})

@group_required('Staff')
def staff_personalinfo_save(request):
	successCode = 0
	if request.method == "POST":
		try:
			request.user.first_name = request.POST['firstName']
			request.user.last_name = request.POST['lastName']
			request.user.email = request.POST['email']
			request.user.save()
			successCode = 1
		except:
			successCode = -1
	else:
		successCode = -2
	return JsonResponse({'success': successCode})

# STAFF COURSES FUNCTIONS
@group_required('Staff')
def staff_course_detail(request, id):
	c = get_object_or_404(Course, pk=id)
	a = c.assignment_set.all()
	e = c.enrollment_set.all()
	return render(request, 'GradeManagement/staff_course_detail.html', {
	"course": c,
	"assignments": a,
	"enrollments": e
	})

@group_required('Staff')
def staff_courses_assignments(request):
	return render(request, 'GradeManagement/staff_courses_assignments.html')

@group_required('Staff')
def staff_courses_assignment_detail(request, id, aid):
	c = get_object_or_404(Course, pk=id)
	a = get_object_or_404(Assignment, pk=aid)
	e = c.enrollment_set.all()
	ag = a.assignmentgrade_set.all()
	return render(request, 'GradeManagement/staff_courses_assignments.html', {
	"course": c,
	"assignment": a,
	"enrollments": e,
	"grades": ag
	})

@login_required
def staff_courses_assignment_save_grades(request):
	return render(request, 'GradeManagement/staff_courses_assignment_save_grade.html')

@login_required
def staff_courses_assignment_create(request):
	if request.method == "POST":
		form = AssignmentForm(request.POST)
		if form.is_valid():
			Assignment = form.save(commit=False)
			Assignment.Title = request.POST['Title']
			Assignment.Due_date = request.POST['Due_date']
			Assignment.Description = request.POST['Description']
			Assignment.save()
			return redirect('GradeManagement/staff_courses_assignment_detail', pk=Assignment.pk)
	else:
		form = AssignmentForm()
	return render(request, 'GradeManagement/staff_courses_assignments_create.html', {'form': form})

@login_required
def staff_courses_assignment_edit(request, pk):
	Edit = get_object_or_404(Assignment, pk=pk)
	if request.method == "POST":
		form = AssignmentForm(request.POST, instance=Edit)
		if form.is_valid():
			Edit = form.save(commit=False)
			Edit.Title = request.POST['Title']
			Edit.Due_date = request.POST['Due_date']
			Edit.Description = request.POST['Description']
			Edit.save()
			return redirect('GradeManagement/staff_courses_assignments.html', pk=Edit.pk)
	else:
		form = AssignmentForm(instance=Edit)
	return render(request, 'GradeManagement/staff_courses_assignments_edit.html', {'form': form})

@group_required('Staff')
def staff_courses_final_grades(request):
	return render(request, 'GradeManagement/staff_courses_final_grades.html')

@group_required('Staff')
def staff_courses_final_grades_save(request):
	return render(request, 'GradeManagement/staff_courses_final_grades.html')

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
	if request.method == "POST":
		form = CourseForm(request.POST)
		if form.is_valid():
			NewCourse = form.save(commit=False)
			NewCourse = request.POST['Name']
			NewCourse = request.POST['Teacher']
			NewCourse = request.POST['SemesterOfCourse']
			NewCourse = form.save()
			return redirect('GradeManagement/staff_administration_courses.html', pk=NewCourse.pk)
	else:
		form = CourseForm()
	return render(request, 'GradeManagement/staff_adminstration_courses_addcourse.html', {'form': form})

@login_required
def staff_adminstration_courses_details(request):
	return render(request, 'GradeManagement/staff_adminstration_courses_details.html')

@login_required
def staff_administration_course_duplicate(request):
	return render(request, 'GradeManagement/staff_administration_course_duplicate.html')

@login_required
def staff_administration_course_edit(request, pk):
	CourseEdit = get_object_or_404(Course, pk=pk)
	if request.method == "POST":
		form = CourseForm(request.POST, instance=CourseEdit)
		if form.is_valid():
			CourseEdit = form.save(commit=False)
			CourseEdit.Name = request.POST['Name']
			CourseEdit.Teacher = request.POST['Teacher']
			CourseEdit.SemesterOfCourse = request.POST['SemesterOfCourse']
			CourseEdit.save()
			return redirect('GradeManagement/staff_administration_courses.html', pk=CourseEdit.pk)
	else:
		form = CourseForm(instance=CourseEdit)
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
