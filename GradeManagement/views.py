from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Course, Enrollment, Assignment, AssignmentGrade, Semester
from django.http import HttpResponse, JsonResponse
from .forms import AssignmentForm, SemesterForm, CourseForm, AddUserForm, EnrollmentForm
from datetime import datetime

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
def student_personalinfo_save(request):
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
	CareerTotalAverage = -1
	if CareerTotalClasses > 0:
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

@group_required('Staff')
def staff_courses_assignment_save_grades(request, id, aid):
	if request.method == "POST":
		c = get_object_or_404(Course, pk=id)
		a = get_object_or_404(Assignment, pk=aid)
		e = c.enrollment_set.all()
		ag = a.assignmentgrade_set.all()
		for key in request.POST:
			if key.startswith('grade'):
				uid = key[5:]
				try:
					value = int(request.POST[key])
					if ag.filter(UserOfAssignment__id=uid).exists():
						curGrade = ag.get(UserOfAssignment__id=uid)
						if value == "":
							curGrade.GradeOfAssignment = None
						else:
							curGrade.GradeOfAssignment = value
						curGrade.save()
					elif value is not "":
						curGrade = AssignmentGrade(UserOfAssignment=User.objects.get(id=uid), Assignment=a, GradeOfAssignment=value)
						curGrade.save()
				except ValueError:
					pass
	return redirect('staff-courses-assignment-detail', id, aid)

@group_required('Staff')
def staff_courses_assignment_create(request, id):
	c = get_object_or_404(Course, pk=id)
	if request.method == "POST":
		form = AssignmentForm(request.POST)
		if form.is_valid():
			a = Assignment()
			a.Title = form.cleaned_data['title']
			a.Due_date = datetime.combine(form.cleaned_data['due_date'], form.cleaned_data['due_time'])
			a.Description = form.cleaned_data['description']
			a.Course = c
			a.save()
			return redirect('staff-courses-assignment-detail', id, a.id)
	else:
		form = AssignmentForm()
	return render(request, 'GradeManagement/staff_courses_assignments_create.html', {
	'form': form,
	"course": c
	})

@group_required('Staff')
def staff_courses_assignment_edit(request, id, aid):
	c = get_object_or_404(Course, pk=id)
	a = get_object_or_404(Assignment, pk=aid)
	if request.method == "POST":
		form = AssignmentForm(request.POST)
		if form.is_valid():
			a.Title = form.cleaned_data['title']
			a.Due_date = datetime.combine(form.cleaned_data['due_date'], form.cleaned_data['due_time'])
			a.Description = form.cleaned_data['description']
			a.save()
			return redirect('staff-courses-assignment-detail', id, a.id)
	else:
		form = AssignmentForm(initial={
			'title': a.Title,
			'description': a.Description,
			'due_date': a.Due_date.date(),
			'due_time': a.Due_date.time()
		})
	return render(request, 'GradeManagement/staff_courses_assignments_edit.html', {
	'form': form,
	'course': c,
	'assignment': a
	})

@group_required('Staff')
def staff_courses_final_grades(request, id):
	c = get_object_or_404(Course, pk=id)
	e = c.enrollment_set.all()
	return render(request, 'GradeManagement/staff_courses_final_grades.html', {
	'course': c,
	'enrollments': e
	})

@group_required('Staff')
def staff_courses_final_grades_save(request, id):
	if request.method == "POST":
		c = get_object_or_404(Course, pk=id)
		e = c.enrollment_set.all()
		for key in request.POST:
			if key.startswith('grade'):
				uid = key[5:]
				try:
					value = int(request.POST[key])
					if e.filter(id=uid).exists():
						enrollment = e.get(id=uid)
						if value == "":
							enrollment.Grade = None
						else:
							enrollment.Grade = value
						enrollment.save()
				except ValueError:
					pass
		return redirect('staff-course-detail', id)
	return redirect('staff-courses-final-grades', id)

# STAFF ADMIN FUNCTIONS
@group_required('Staff')
def staff_administration(request):
	return render(request, 'GradeManagement/admin_home.html')

@group_required('Staff')
def admin_courses(request):
	return render(request, 'GradeManagement/admin_courses.html', {
	'active_courses': Course.objects.filter(SemesterOfCourse__Active=True),
	'inactive_courses': Course.objects.filter(SemesterOfCourse__Active=False)
	})

@group_required('Staff')
def admin_course_detail(request, id):
	c = get_object_or_404(Course, pk=id)
	en = c.enrollment_set.all()
	a = c.assignment_set.all()
	return render(request, 'GradeManagement/admin_course_detail.html', {
	'course': c,
	'enrollments': en,
	'assignments': a
	})

@group_required('Staff')
def admin_course_enrollments(request, id):
	c = get_object_or_404(Course, pk=id)
	en = c.enrollment_set.all()
	if request.method == "POST":
		print(request.POST)
		form = EnrollmentForm(request.POST)
		if form.is_valid():
			e = Enrollment()
			e.Students = form.cleaned_data['student']
			e.Course = form.cleaned_data['course']
			if form.cleaned_data['grade'] is not None:
				e.Grade = form.cleaned_data['grade']
			e.save()
	form = EnrollmentForm(initial={
		'course': c
	})
	form['course'].field.widget.attrs['readonly'] = 'readonly'
	usersEnrolled = User.objects.filter(pk__in=set(en.values_list('Students', flat=True)))
	form['student'].field.queryset = User.objects.filter(groups__name='Student').difference(usersEnrolled)
	return render(request, 'GradeManagement/admin_course_enrollments.html', {
	'course': c,
	'enrollments': en,
	'form': form
	})

@group_required('Staff')
def admin_course_create(request):
	if request.method == "POST":
		form = CourseForm(request.POST)
		if form.is_valid():
			c = Course()
			c.Name = form.cleaned_data['name']
			c.Teacher = form.cleaned_data['teacher']
			c.SemesterOfCourse = form.cleaned_data['semester']
			c.save()
			return redirect('admin-course-detail', c.id)
	else:
		form = CourseForm()
	return render(request, 'GradeManagement/admin_course_create.html', {
	'form': form,
	})

@group_required('Staff')
def admin_course_enrollments_delete(request, id):
	successCode = 0
	if request.method == "POST":
		try:
			e = Enrollment.objects.get(pk=request.POST['eid'])
			e.delete()
			successCode = 1
		except Exception as ex:
			successCode = -1
	else:
		successCode = -2
	return JsonResponse({'success': successCode})

@group_required('Staff')
def admin_users(request):
	StudentUsers = User.objects.filter(groups__name='Student')
	StaffUsers = User.objects.filter(groups__name='Staff')
	Allusers = User.objects.all()
	return render(request, "GradeManagement/admin_users.html", {
	'StudentList': StudentUsers,
	'StaffList': StaffUsers})

@group_required('Staff')
def admin_users_create(request):
	if request.method == "POST":
		form = AddUserForm(request.POST)
		if form.is_valid():
			u = User()
			u.username = form.cleaned_data['username']
			u.first_name = form.cleaned_data['firstname']
			u.last_name = form.cleaned_data['lastname']
			u.email = form.cleaned_data['email']
			u.password = form.cleaned_data['password']
			u.save()
			group = form.cleaned_data['Group']
			group.save()
			group.user_set.add(u)
			return redirect('admin-users')
	else:
		form = AddUserForm()
	return render(request, 'GradeManagement/admin_users_create.html', {'form': form})

@group_required('Staff')
def admin_semesters(request):
	ActiveSemester = Semester.objects.filter(Active=True)
	InactiveSemester = Semester.objects.filter(Active=False)
	return render(request, 'GradeManagement/admin_semesters.html', {
	'ActiveSemester': ActiveSemester,
	'InactiveSemester': InactiveSemester,
	})

@group_required('Staff')
def admin_enrollments(request):
	pass

@group_required('Staff')
def admin_course_edit(request):
	pass

## STAFF ON USER FUNCTIONS
@group_required('Staff')
def staff_administration_users(request):
	return render(request, 'GradeManagement/staff_administration_users.html')

@group_required('Staff')
def staff_administration_users_addUser(request):
	if request.method == "POST":
		form = AddUserForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('GradeManagement/staff_administration_users.html')
		else:
			form = AddUserForm()
	return render(request, 'GradeManagement/staff_administration_users_addUser.html', {'form': form})

@group_required('Staff')
def staff_administration_users_addUser_save(request):
	return render(request, 'GradeManagement/staff_administration_users_addUser_save.html')

@group_required('Staff')
def staff_administration_users_details(request):
	return render(request, 'GradeManagement/staff_administration_users_details.html')

@group_required('Staff')
def staff_administration_users_details_editUser(request):
	if request.method == "POST":
		form = EditUserForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			return redirect('GradeManagement/staff_administration_users.html')
	else:
		form = EditUserForm(instance=request.user)
	return render(request, 'GradeManagement/staff_administration_users_details_editUser.html', {'form': form})

@group_required('Staff')
def staff_administration_users_details_deactivateUser(request):
	return render(request, 'GradeManagement/staff_administration_users_details_deactivateUser.html')


## STAFF ON COURSE FUNCTIONS
@group_required('Staff')
def staff_administration_courses(request):
	return render(request, 'GradeManagement/staff_administration_courses.html')

@group_required('Staff')
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

@group_required('Staff')
def staff_adminstration_courses_details(request):
	return render(request, 'GradeManagement/staff_adminstration_courses_details.html')

@group_required('Staff')
def staff_administration_course_duplicate(request):
	return render(request, 'GradeManagement/staff_administration_course_duplicate.html')

@group_required('Staff')
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
@group_required('Staff')
def staff_administration_semesters(request):
	return render(request, 'GradeManagement/staff_administration_semesters.html')

@group_required('Staff')
def admin_semesters_create(request):
	if request.method == "POST":
		form = SemesterForm(request.POST)
		if form.is_valid():
			s = Semester()
			s.Title = form.cleaned_data['title']
			s.StartDate = form.cleaned_data['start_date']
			s.EndDate = form.cleaned_data['end_date']
			s.Active = form.cleaned_data['active']
			s.save()
			return redirect('admin-semesters')
	else:
		form = SemesterForm()
	return render(request, 'GradeManagement/admin_semesters_create.html', {'form': form})

@group_required('Staff')
def admin_semesters_activity(request):
	if request.method == "POST":
		try:
			if request.POST["method"] == "active":
				s = Semester.objects.get(pk=request.POST["semester"])
				s.Active = True
				s.save()
			elif request.POST["method"] == "inactive":
				s = Semester.objects.get(pk=request.POST["semester"])
				s.Active = False
				s.save()
			else:
				return JsonResponse({"success": -1})
			return JsonResponse({"success": 1})
		except:
			return JsonResponse({"success": -1})
	return JsonResponse({"success": -2})

####################
# END: STAFF VIEWS #
####################
