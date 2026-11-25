from django.urls import path
from . import views

app_name = 'enquiries'

urlpatterns = [
    path('', views.enquiry_list, name='list'),
    path('<int:pk>/status/', views.enquiry_update_status, name='update_status'),
    path('<int:pk>/delete/', views.enquiry_delete, name='delete'),
    path('messages/', views.contact_messages_list, name='messages'),
    path('messages/<int:pk>/toggle/', views.toggle_message_read, name='toggle_read'),
    path('messages/<int:pk>/delete/', views.contact_message_delete, name='delete_message'),
]
