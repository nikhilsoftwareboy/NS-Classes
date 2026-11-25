"""
Root URL configuration for NS Classes project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django built-in admin
    path('django-admin/', admin.site.urls),

    # Authentication (/login/, /logout/, /register/, /profile/)
    path('', include('accounts.urls')),

    # Role-based Dashboards (/dashboard/, /admin/dashboard/, /teacher/dashboard/, /student/dashboard/)
    path('dashboard/', include('dashboard.urls')),
    path('admin/dashboard/', include('dashboard.urls_admin')),
    path('teacher/dashboard/', include('dashboard.urls_teacher')),
    path('student/dashboard/', include('dashboard.urls_student')),

    # Management Modules
    path('students/', include('students.urls')),
    path('manage-teachers/', include('teachers.urls')),
    path('manage-courses/', include('courses.urls')),
    path('batches/', include('batches.urls')),
    path('timetable/', include('timetable.urls')),
    path('attendance/', include('attendance.urls')),
    path('fees/', include('fees.urls')),
    path('enquiries/', include('enquiries.urls')),
    path('materials/', include('materials.urls')),
    path('announcements/', include('announcements.urls')),

    # Public website pages (home, about, courses, teachers, gallery, contact, admission, etc.)
    path('', include('website.urls')),
]

# Serve media and static files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
