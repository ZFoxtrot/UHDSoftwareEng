from django import template
from GradeManagement.models import Course, Enrollment, Assignment, AssignmentGrade, Semester

register = template.Library()

@register.filter
def grade_select(value, arg):
	try:
		ret = value.get(UserOfAssignment=arg)
		return ret.GradeOfAssignment
	except AssignmentGrade.DoesNotExist:
		return ""
