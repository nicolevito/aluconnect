from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from courses.models import Course
from .models import Lesson
from .serializers import LessonSerializer

class LessonListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"detail": "Curso não encontrado"}, status=status.HTTP_404_NOT_FOUND)

        lessons = course.lessons.all()
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)

    def post(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"detail": "Curso não encontrado"}, status=status.HTTP_404_NOT_FOUND)

        serializer = LessonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(course=course)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LessonDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, course_id, lesson_id):
        try:
            return Lesson.objects.get(id=lesson_id, course_id=course_id)
        except Lesson.DoesNotExist:
            return None

    def get(self, request, course_id, lesson_id):
        lesson = self.get_object(course_id, lesson_id)
        if not lesson:
            return Response({"detail": "Aula não encontrada"}, status=status.HTTP_404_NOT_FOUND)
        serializer = LessonSerializer(lesson)
        return Response(serializer.data)

    def put(self, request, course_id, lesson_id):
        lesson = self.get_object(course_id, lesson_id)
        if not lesson:
            return Response({"detail": "Aula não encontrada"}, status=status.HTTP_404_NOT_FOUND)

        serializer = LessonSerializer(lesson, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, course_id, lesson_id):
        lesson = self.get_object(course_id, lesson_id)
        if not lesson:
            return Response({"detail": "Aula não encontrada"}, status=status.HTTP_404_NOT_FOUND)
        lesson.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
