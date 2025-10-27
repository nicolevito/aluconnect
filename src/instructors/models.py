from django.db import models


class Instructor(models.Model):
    name = models.CharField(max_length=50)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)