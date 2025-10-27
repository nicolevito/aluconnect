from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Course, Enrollment
from .serializers import CourseSerializer, EnrollmentSerializer
from authentication.models import UserProfile
from students.models import Students

class CourseCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            course = serializer.save()
            # Se quiser adicionar instrutores ao criar:
            if "instructor_ids" in request.data:
                for user_id in request.data["instructor_ids"]:
                    profile = UserProfile.objects.get(user_id=user_id)
                    course.instructors.add(profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CourseListAPIView(APIView):
    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

class CourseDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Response({"detail": "Curso não encontrado"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CourseSerializer(course)
        return Response(serializer.data)

class CourseUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Response({"detail": "Curso não encontrado"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EnrollAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Response({"detail": "Curso não encontrado"}, status=status.HTTP_404_NOT_FOUND)
        profile = UserProfile.objects.get(user=request.user)
        enrollment, created = Enrollment.objects.get_or_create(course=course, student=profile)
        serializer = EnrollmentSerializer(enrollment)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

class StudentCoursesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        from authentication.models import UserProfile
        profile = UserProfile.objects.get(user_id=pk)

        student = Students.objects.get(user=profile.user)

        courses = [e.course for e in student.enrollments.all()]
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

class InstructorCoursesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            profile = UserProfile.objects.get(user_id=pk, is_instructor=True)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Instrutor não encontrado"}, status=status.HTTP_404_NOT_FOUND)

        courses = profile.courses_created.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)