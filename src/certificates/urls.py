from django.urls import path
from .views import GenerateCertificateAPIView, ListCertificatesAPIView

urlpatterns = [
    path('generate/<int:student_id>/<int:course_id>/', GenerateCertificateAPIView.as_view(), name='generate-certificate'),
    path('list/<int:student_id>/', ListCertificatesAPIView.as_view(), name='list-certificates'),
]
