from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .tasks import generate_certificate
from .models import Certificate
from .serializers import CertificateSerializer
from authentication.models import UserProfile

class GenerateCertificateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, student_id, course_id):
        try:
            student = UserProfile.objects.get(user_id=student_id)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Aluno não encontrado"}, status=status.HTTP_404_NOT_FOUND)

        task = generate_certificate.delay(student.user_id, course_id)
        return Response({"task_id": task.id, "detail": "Certificado adicionado à fila"}, status=status.HTTP_202_ACCEPTED)

class ListCertificatesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, student_id):
        try:
            student = UserProfile.objects.get(user_id=student_id)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Aluno não encontrado"}, status=status.HTTP_404_NOT_FOUND)

        certificates = Certificate.objects.filter(student=student)
        serializer = CertificateSerializer(certificates, many=True)
        return Response(serializer.data)
