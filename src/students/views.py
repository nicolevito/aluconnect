from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from authentication.models import User
from rest_framework.permissions import IsAuthenticated
from authentication.custom_auth import TokenAuthentication

from .serializers import StudentSerializer

class StudentListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        students = User.objects.filter(userprofile__is_instructor=False)
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

class StudentDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, pk):
        try:
            student = User.objects.get(pk=pk, userprofile__is_instructor=False)
        except User.DoesNotExist:
            return Response({'detail': 'Aluno não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StudentSerializer(student)
        return Response(serializer.data)

class StudentCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        from authentication.models import UserProfile
        UserProfile.objects.get_or_create(user=user, is_instructor=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class StudentUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def put(self, request, pk):
        try:
            student = User.objects.get(pk=pk, userprofile__is_instructor=False)
        except User.DoesNotExist:
            return Response({'detail': 'Aluno não encontrado'}, status=status.HTTP_404_NOT_FOUND)

        serializer = StudentSerializer(student, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
