from django.urls import path
from .views import StudentListAPIView, StudentDetailAPIView, StudentCreateAPIView, StudentUpdateAPIView

urlpatterns = [
    path('', StudentListAPIView.as_view(), name='student-list'),
    path('<int:pk>/', StudentDetailAPIView.as_view(), name='student-detail'),
    path('create/', StudentCreateAPIView.as_view(), name='student-create'),
    path('<int:pk>/update/', StudentUpdateAPIView.as_view(), name='student-update'),
]