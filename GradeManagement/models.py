from django.db import models
from django.contrib.auth.models import User, Group, Permission


class Semester(models.Model):
    Title = models.CharField(max_length=256)
    StartDate = models.DateTimeField()
    EndDate = models.DateTimeField()

    def __str__(self):
        return 'Semester: {}'.format(self.Title)

# Field null=True is required for on_delete=models.SET_NULL to work
# on_delete=models.CASCADE probably won't require it but I haven't tested it


class Course(models.Model):
    Name = models.CharField(max_length=256)
    Teacher = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    SemesterOfCourse = models.ForeignKey(Semester, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return 'Course: {}'.format(self.Name)


class Assignment(models.Model):
    Title = models.CharField(max_length=256)
    Due_date = models.DateTimeField()
    Description = models.TextField()
    Course = models.ForeignKey(Course, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return 'Course: {}'.format(self.Title)


class AssignmentGrade(models.Model):
    Assignment = models.ManyToManyField(Assignment)
    UserOfAssignment = models.ManyToManyField(User)
    # default=None sets field to None if no value is given
    # blank=True allows field to be empty given no input
    # null=True means database row is allowed to be null
    # set one of these for default grade to be nothing
    GradeOfAssignment = models.IntegerField(null=True)


class Enrollment(models.Model):
    Students = models.ManyToManyField(User)
    Course = models.ManyToManyField(Course)
    Grade = models.IntegerField(null=True)
