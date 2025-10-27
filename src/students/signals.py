from django.db.models.signals import post_save
from django.dispatch import receiver
from authentication.models import User
from .models import Students

@receiver(post_save, sender=User)
def create_student(sender, instance, created, **kwargs):
    if created:
        Students.objects.create(user=instance)
