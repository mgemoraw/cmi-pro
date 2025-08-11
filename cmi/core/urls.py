from django.urls import path
from . import views


app_name = 'core'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('truck/', views.trucks, name='truck'),
    path('truck/create/', views.trucks, name='truck_create'),
]