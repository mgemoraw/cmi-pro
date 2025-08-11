from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('services/', views.services, name='services'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
