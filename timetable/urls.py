from django.urls import path
from . import views

app_name = 'timetable'

urlpatterns = [
    path('', views.timetable_index, name='index'),
    path('add/', views.timetable_create, name='create'),
    path('<int:pk>/edit/', views.timetable_update, name='update'),
    path('<int:pk>/delete/', views.timetable_delete, name='delete'),
]
