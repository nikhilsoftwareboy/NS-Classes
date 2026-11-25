from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('courses/', views.courses_list, name='courses'),
    path('courses/<int:pk>/', views.course_detail, name='course_detail'),
    path('teachers/', views.teachers_list, name='teachers'),
    path('gallery/', views.gallery_view, name='gallery'),
    path('contact/', views.contact_view, name='contact'),
    path('admission/', views.admission_view, name='admission'),
    path('faq/', views.faq_view, name='faq'),
    path('privacy/', views.privacy_policy, name='privacy'),
    path('terms/', views.terms_conditions, name='terms'),
]
