from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, UserProfile
import secrets

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        token = secrets.token_hex(32)  
        UserProfile.objects.get_or_create(user=instance, api_token=token)
