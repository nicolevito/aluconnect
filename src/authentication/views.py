# authentication/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer, RegisterSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from authentication.permissions import IsInstructor, IsStudent

@method_decorator(csrf_exempt, name='dispatch')
class RegisterAPIView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh), 'access': str(refresh.access_token),
            'username': user.username, 'role': user.role
        }, status=status.HTTP_201_CREATED)


@method_decorator(csrf_exempt, name='dispatch')
class LoginAPIView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),'access': str(refresh.access_token),
            'username': user.username,'role': user.role
        }, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    permission_classes = []

    def post(self, request):
        return Response({"detail": "Logout realizado com sucesso"}, status=status.HTTP_200_OK)

class LessonCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsInstructor]

    def post(self, request, course_id):
        return Response({"detail": "Aula criada com sucesso"})
    
class StudentCoursesAPIView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request):
        return Response({"courses": []})