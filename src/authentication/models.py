from django.db import models
from django.contrib.auth.models import AbstractUser
import secrets 

class User(AbstractUser):
    ROLE_CHOICES = (('ADMIN', 'Admin'),('INSTRUCTOR', 'Instructor'),('STUDENT', 'Student'),)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='STUDENT')

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=50, blank=True, null=False)
    last_name = models.CharField(max_length=50, blank=True, null=False)
    is_instructor = models.BooleanField(default=False)
    phone = models.CharField(max_length=20, blank=True, null=True)
    profile_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    api_token = models.CharField(max_length=64, unique=True, null=True, blank=True)
