from django.urls import path
from .views import (StudentProgressListAPIView, StudentCourseProgressAPIView, 
    RegisterLessonProgressAPIView
)

urlpatterns = [
    path('courses/<int:course_id>/lessons/<int:lesson_id>/progress', RegisterLessonProgressAPIView.as_view(), name='lesson-progress'),

    path('students/<int:student_id>/progress', StudentProgressListAPIView.as_view(), name='student-progress'),

    path('students/<int:student_id>/courses/<int:course_id>/progress', StudentCourseProgressAPIView.as_view(), name='student-course-progress'),
]
