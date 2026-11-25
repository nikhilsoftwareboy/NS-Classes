from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('manage/', views.course_manage_list, name='manage_list'),
    path('add/', views.course_create, name='create'),
    path('<int:pk>/edit/', views.course_update, name='update'),
    path('<int:pk>/delete/', views.course_delete, name='delete'),
]
