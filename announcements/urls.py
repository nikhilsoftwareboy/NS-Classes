from django.urls import path
from . import views

app_name = 'announcements'

urlpatterns = [
    path('', views.announcement_list, name='list'),
    path('add/', views.announcement_create, name='create'),
    path('<int:pk>/delete/', views.announcement_delete, name='delete'),
]
