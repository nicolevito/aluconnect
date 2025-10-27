# students/models.py
from django.db import models
from authentication.models import User
from courses.models import Course

class Students(models.Model):
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='main_students', null=True, blank=True)
    enrolled_courses = models.ManyToManyField('courses.Course', through='Enrollment',related_name='enrolled_students')

class Enrollment(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.user.username} -> {self.course.name}"
