
from django.db import models
from authentication.models import UserProfile, User

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    instructors = models.ManyToManyField(UserProfile, related_name='courses_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # <-- aqui

class Enrollment(models.Model):
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='student_enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='student_course_enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
