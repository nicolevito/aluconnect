# lessons/urls.py
from django.urls import path
from .views import LessonListCreateAPIView, LessonDetailAPIView

urlpatterns = [
    path('', LessonListCreateAPIView.as_view(), name='lesson-list-create'),
    path('<int:lesson_id>/', LessonDetailAPIView.as_view(), name='lesson-detail'),
]
