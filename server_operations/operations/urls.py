from django.urls import path
from . import views

app_name = 'operations'

urlpatterns = [
    path('', views.operation_list, name='operation_list'),
    path('statistics/', views.statistics, name='statistics'),
    path('<slug:slug>/', views.operation_detail, name='operation_detail'),
]