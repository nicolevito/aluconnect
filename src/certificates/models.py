from django.db import models
from authentication.models import UserProfile
from courses.models import Course

class Certificate(models.Model):
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='certificates')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='certificates')
    content = models.TextField()  
    created_at = models.DateTimeField(auto_now_add=True)
    delivered = models.BooleanField(default=False)  

    def __str__(self):
        return f"Certificado para {self.student.user.username} no curso {self.course.title}"