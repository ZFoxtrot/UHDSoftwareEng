from django.db import models
from django.contrib.auth.models import User, Group, Permission


class Semester(models.Model):
    Title = models.CharField(max_length=256)
    StartDate = models.DateTimeField()
    EndDate = models.DateTimeField()
    Active = models.BooleanField(default=False)

    def __str__(self):
        return '{}'.format(self.Title)

# Field null=True is required for on_delete=models.SET_NULL to work
# on_delete=models.CASCADE probably won't require it but I haven't tested it


class Course(models.Model):
    Name = models.CharField(max_length=256)
    Teacher = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    SemesterOfCourse = models.ForeignKey(Semester, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return '{}/{}'.format(self.Name, self.SemesterOfCourse)


class Assignment(models.Model):
    Title = models.CharField(max_length=256)
    Due_date = models.DateTimeField()
    Description = models.TextField()
    Course = models.ForeignKey(Course, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return '{}/{}'.format(self.Course, self.Title)


class AssignmentGrade(models.Model):
    Assignment = models.ForeignKey(Assignment, null=True, on_delete=models.SET_NULL)
    UserOfAssignment = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    # default=None sets field to None if no value is given
    # blank=True allows field to be empty given no input
    # null=True means database row is allowed to be null
    # set one of these for default grade to be nothing
    GradeOfAssignment = models.IntegerField(null=True)

    def __str__(self):
        return '{}/{}/{}'.format(self.Assignment, self.UserOfAssignment, self.GradeOfAssignment)


class Enrollment(models.Model):
    Students = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    Course = models.ForeignKey(Course, null=True, on_delete=models.SET_NULL)
    Grade = models.IntegerField(null=True, default=-1)

    def __str__(self):
        return '{} @ {}'.format(self.Students, self.Course)
