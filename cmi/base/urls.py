from django.urls import path

from . import views

appname = 'base'

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
    path('settings/', views.settings, name='settings'),
    path('data-instance/', views.data_instance, name='data_instance'),
    path('equipment/', views.equipment, name='equipment'),
    path('equipment/truck/', views.equipment, name='truck'),
    path('equipment/excavator/', views.equipment, name='excavator'),
    path('equipment/dozer/', views.equipment, name='dozer'),    
    path('equipment/labor/', views.equipment, name='labor'),

    path('work-items/', views.work_items, name='work_items'),
    path('work-orders/', views.work_orders, name='work_orders'),
    path('reports/', views.reports, name='reports'),
]
