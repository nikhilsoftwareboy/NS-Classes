from django.urls import path
from . import views

app_name = 'batches'

urlpatterns = [
    path('', views.batch_list, name='list'),
    path('add/', views.batch_create, name='create'),
    path('<int:pk>/', views.batch_detail, name='detail'),
    path('<int:pk>/edit/', views.batch_update, name='update'),
    path('<int:pk>/delete/', views.batch_delete, name='delete'),
    path('<int:batch_id>/assign/', views.assign_student, name='assign_student'),
]
