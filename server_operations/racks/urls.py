from django.urls import path
from . import views

app_name = 'racks'

urlpatterns = [
    path('', views.rack_list, name='rack_list'),
]