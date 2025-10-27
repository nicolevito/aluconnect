import pytest
from django.utils import timezone
from authentication.models import User, UserProfile
from courses.models import Course
from certificates.models import Certificate
from certificates.tasks import generate_certificate

@pytest.fixture
def user(db):
    u = User.objects.create_user(username="certuser", password="123")
    profile, _ = UserProfile.objects.get_or_create(user=u)
    return u

@pytest.fixture
def course(db):
    return Course.objects.create(title="Curso de Teste")

@pytest.mark.django_db
def test_generate_certificate(monkeypatch, user, course):
    # Mock do OpenAI para não chamar API real
    class FakeResponse:
        choices = [type("obj", (), {"message": {"content": "Certificado gerado"}})()]

    def fake_chatcompletion_create(*args, **kwargs):
        return FakeResponse()

    import openai
    monkeypatch.setattr(openai.ChatCompletion, "create", fake_chatcompletion_create)

    generate_certificate(user.id, course.id)

    profile = UserProfile.objects.get(user=user)
    cert = Certificate.objects.get(student=profile, course=course)
    assert "Certificado" in cert.content
    assert cert.created_at is not None
