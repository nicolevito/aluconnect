from django.urls import path
from .views import InstructorListAPIView, InstructorDetailAPIView, InstructorCreateAPIView, InstructorUpdateAPIView

urlpatterns = [
    path('', InstructorListAPIView.as_view(), name='instructor-list'),
    path('<int:pk>/', InstructorDetailAPIView.as_view(), name='instructor-detail'),
    path('create/', InstructorCreateAPIView.as_view(), name='instructor-create'),
    path('<int:pk>/update/', InstructorUpdateAPIView.as_view(), name='instructor-update'),
]
