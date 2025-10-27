from rest_framework import serializers
from authentication.models import User

class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff']  # is_staff pode indicar instrutor/admin
