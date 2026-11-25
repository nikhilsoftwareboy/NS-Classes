from django.urls import path
from . import views

app_name = 'fees'

urlpatterns = [
    path('', views.fee_list, name='list'),
    path('add/', views.fee_create, name='create'),
    path('<int:pk>/pay/', views.record_payment, name='pay'),
    path('<int:pk>/receipt/', views.fee_receipt, name='receipt'),
]
