# student_progress/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from authentication.models import User
from courses.models import Course
from lessons.models import Lesson
from .models import Progress
from .serializers import ProgressSerializer
from authentication.models import UserProfile
from certificates.tasks import generate_certificate


class RegisterLessonProgressAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id, lesson_id):
        user = request.user
        try:
            lesson = Lesson.objects.get(id=lesson_id, course_id=course_id)
        except Lesson.DoesNotExist:
            return Response({"detail": "Aula não encontrada"}, status=status.HTTP_404_NOT_FOUND)

        profile = UserProfile.objects.get(user=user)
        progress, created = Progress.objects.get_or_create(student=profile, lesson=lesson)
        progress.completed = True
        progress.save()
        serializer = ProgressSerializer(progress)

        all_lessons = lesson.course.lessons.all()
        completed_lessons = Progress.objects.filter(student=profile, lesson__course=lesson.course, completed=True)

        if completed_lessons.count() == all_lessons.count():
            generate_certificate.delay(profile.user_id, lesson.course.id)

        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

class StudentProgressListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, student_id):
        try:
            user = User.objects.get(id=student_id)
            profile = UserProfile.objects.get(user=user)
        except User.DoesNotExist:
            return Response({"detail": "Aluno não encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Perfil de aluno não encontrado"}, status=status.HTTP_404_NOT_FOUND)

        progress = Progress.objects.filter(student=profile)
        serializer = ProgressSerializer(progress, many=True)
        return Response(serializer.data)


class StudentCourseProgressAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, student_id, course_id):
        try:
            user = User.objects.get(id=student_id)
            profile = UserProfile.objects.get(user=user)
        except User.DoesNotExist:
            return Response({"detail": "Aluno não encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Perfil de aluno não encontrado"}, status=status.HTTP_404_NOT_FOUND)

        progress = Progress.objects.filter(student=profile, lesson__course_id=course_id)
        serializer = ProgressSerializer(progress, many=True)
        return Response(serializer.data)
