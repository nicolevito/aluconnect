from django.contrib import admin
from django.urls import path, include
from courses.views import StudentCoursesAPIView, InstructorCoursesAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')), 
    path('api/students/', include('students.urls')),
    path('api/instructors/', include('instructors.urls')),
    path('api/courses/', include('courses.urls')),
    path('api/students/<int:pk>/courses/', StudentCoursesAPIView.as_view(), name='student-courses'),
    path('api/instructors/<int:pk>/courses/', InstructorCoursesAPIView.as_view(), name='instructor-courses'),
    path('api/', include('progress.urls')), 
    path('api/certificates/', include('certificates.urls')),
]
