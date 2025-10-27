from rest_framework import serializers
from .models import Course, Enrollment
from authentication.models import UserProfile

class CourseSerializer(serializers.ModelSerializer):
    instructors = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='user__username'
    )

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'instructors', 'price', 'created_at', 'updated_at']


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'enrolled_at']
