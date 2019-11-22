from django import template
from GradeManagement.models import Course, Enrollment, Assignment, AssignmentGrade, Semester

register = template.Library()

@register.filter
def grade_select(value, arg):
	try:
		ret = value.get(UserOfAssignment=arg)
		if ret.GradeOfAssignment is None:
			return ""
		return ret.GradeOfAssignment
	except AssignmentGrade.DoesNotExist:
		return ""

@register.filter
def grade_translate(value):
	if value >= 0:
		return value
	return ""
