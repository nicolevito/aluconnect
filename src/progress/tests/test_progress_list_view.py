import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from authentication.models import UserProfile, User
from courses.models import Course
from lessons.models import Lesson
from progress.models import Progress

@pytest.mark.django_db
def test_student_progress_list():
    client = APIClient()

    user = User.objects.create_user(username='progressuser', password='1234')
    profile, _ = UserProfile.objects.get_or_create(user=user)

    course = Course.objects.create(title='Django Avançado', description='Curso top')
    lesson = Lesson.objects.create(course=course, title='Aula 1')

    Progress.objects.create(student=profile, lesson=lesson, completed=True)

    url = reverse('student-progress', args=[profile.user_id])
    client.force_authenticate(user=user)
    response = client.get(url)

    assert response.status_code == 200
    assert any(item["lesson"] == lesson.id for item in response.data)
