import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from authentication.models import User, UserProfile
from courses.models import Course
from lessons.models import Lesson
from progress.models import Progress

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    u = User.objects.create_user(username="testuser", password="123")
    profile, _ = UserProfile.objects.get_or_create(user=u)
    return u

@pytest.fixture
def course(db):
    return Course.objects.create(title="Curso Teste")

@pytest.fixture
def lesson(db, course):
    return Lesson.objects.create(title="Aula Teste", course=course)

@pytest.mark.django_db
def test_register_lesson_progress(api_client, user, course, lesson):
    api_client.force_authenticate(user=user)
    url = reverse('lesson-progress', args=[course.id, lesson.id])
    response = api_client.post(url)
    assert response.status_code in [200, 201]
    profile = UserProfile.objects.get(user=user)
    progress = Progress.objects.get(student=profile, lesson=lesson)
    assert progress.completed is True
