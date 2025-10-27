# courses/urls.py
from django.urls import path, include
from .views import (
    CourseCreateAPIView, CourseListAPIView, CourseDetailAPIView,
    CourseUpdateAPIView, EnrollAPIView, StudentCoursesAPIView, InstructorCoursesAPIView
)

urlpatterns = [
    path('', CourseListAPIView.as_view(), name='course-list'),
    path('create/', CourseCreateAPIView.as_view(), name='course-create'),
    path('<int:pk>/', CourseDetailAPIView.as_view(), name='course-detail'),
    path('<int:pk>/update/', CourseUpdateAPIView.as_view(), name='course-update'),
    path('<int:pk>/enroll/', EnrollAPIView.as_view(), name='course-enroll'),
    path('students/<int:pk>/', StudentCoursesAPIView.as_view(), name='student-courses'),
    path('instructors/<int:pk>/', InstructorCoursesAPIView.as_view(), name='instructor-courses'),
    path('<int:course_id>/lessons/', include('lessons.urls')),
]
