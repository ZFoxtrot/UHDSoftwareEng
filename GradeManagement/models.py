from django.db import models
from django.contrib.auth.models import User, Group, Permission


class Semester(models.Model):
    Title = models.CharField(max_length=256)
    StartDate = models.DateTimeField()
    EndDate = models.DateTimeField()


class Course(models.Model):
    Name = models.CharField(max_length=256)
    Teacher = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    SemesterOfCourse = models.ForeignKey(Semester, null=True, on_delete=models.SET_NULL)


class Assignment(models.Model):
    Title = models.CharField(max_length=256)
    Due_date = models.DateTimeField()
    Description = models.TextField()
    Course = models.ForeignKey(Course, null=True, on_delete=models.SET_NULL)


class AssignmentGrade(models.Model):
    Assignment = models.ForeignKey(Assignment, null=True, on_delete=models.SET_NULL)
    UserOfAssignment = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    GradeOfAssignment = models.IntegerField()
