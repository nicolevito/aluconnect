# authentication/permissions.py
from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == 'ADMIN')

class IsInstructor(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == 'INSTRUCTOR')

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == 'STUDENT')
