
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from authentication.models import User, UserProfile
from .serializers import InstructorSerializer
from rest_framework.permissions import IsAuthenticated

class InstructorListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        instructors = User.objects.filter(userprofile__is_instructor=True)
        serializer = InstructorSerializer(instructors, many=True)
        return Response(serializer.data)


class InstructorDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            instructor = User.objects.get(pk=pk, userprofile__is_instructor=True)
        except User.DoesNotExist:
            return Response({"detail": "Instrutor não encontrado"}, status=status.HTTP_404_NOT_FOUND)
        serializer = InstructorSerializer(instructor)
        return Response(serializer.data)


class InstructorCreateAPIView(APIView):
    permission_classes = [IsAuthenticated] 

    def post(self, request):
        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"detail": "Usuário não encontrado"}, status=status.HTTP_404_NOT_FOUND)
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.is_instructor = True
        profile.save()
        serializer = InstructorSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class InstructorUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            instructor = User.objects.get(pk=pk, userprofile__is_instructor=True)
        except User.DoesNotExist:
            return Response({"detail": "Instrutor não encontrado"}, status=status.HTTP_404_NOT_FOUND)

        serializer = InstructorSerializer(instructor, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
