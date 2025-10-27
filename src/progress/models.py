from django.db import models
from courses.models import UserProfile
from lessons.models import Lesson
from django.utils import timezone

class Progress(models.Model):
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='lesson_progress')
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(default=timezone.now)  # evita prompt

    class Meta:
        unique_together = ('student', 'lesson')

    def __str__(self):
        return f"{self.student.user.username} - {self.lesson.title} ({'Concluído' if self.completed else 'Em andamento'})"
