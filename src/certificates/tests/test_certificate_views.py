import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from authentication.models import UserProfile, User
from courses.models import Course
from certificates.models import Certificate

@pytest.mark.django_db
def test_list_certificates_view():
    client = APIClient()

    user, created = User.objects.get_or_create(username='testuser')
    if created:
        user.set_password('1234')
        user.save()

    profile, created = UserProfile.objects.get_or_create(user=user)

    course = Course.objects.create(title='Python Básico', description='Intro')
    Certificate.objects.create(student=profile, course=course, content='Certificado teste')

    url = reverse('list-certificates', args=[profile.user_id])
    client.force_authenticate(user=user)
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data) >= 1
    assert 'Certificado teste' in str(response.data)
