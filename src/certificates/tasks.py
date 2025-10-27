# certificates/tasks.py
from celery import shared_task
from django.utils import timezone
from authentication.models import UserProfile
from courses.models import Course
from .models import Certificate
import openai
import os
from openai.error import OpenAIError, RateLimitError, InvalidRequestError, AuthenticationError

openai.api_key = os.getenv("OPENAI_API_KEY")

@shared_task
def generate_certificate(user_id, course_id):
    try:
        profile = UserProfile.objects.get(user_id=user_id)
        course = Course.objects.get(id=course_id)
    except (UserProfile.DoesNotExist, Course.DoesNotExist):
        return f"Perfil ou curso não encontrado: user_id={user_id}, course_id={course_id}"

    prompt = f"""
    Gere um texto de certificado de conclusão para o aluno {profile.user.username} 
    ({profile.user.first_name} {profile.user.last_name}) que concluiu o curso "{course.title}".
    O texto deve ser formal, motivacional e pronto para compartilhar nas redes sociais.
    """

    certificate_text = None

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=250
        )

        choice = response["choices"][0] if isinstance(response, dict) else response.choices[0]
        message = choice["message"] if isinstance(choice, dict) else choice.message
        content = message["content"] if isinstance(message, dict) else message.content

        certificate_text = content.strip()

    except (RateLimitError, InvalidRequestError, AuthenticationError, OpenAIError):
        certificate_text = (
            f"Certificado de conclusão do curso '{course.title}' concedido a "
            f"{profile.user.first_name} {profile.user.last_name}."
        )

    Certificate.objects.create(
        student=profile,
        course=course,
        content=certificate_text,
        created_at=timezone.now()
    )

    return f"Certificado gerado para {profile.user.username}"