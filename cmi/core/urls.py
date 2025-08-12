from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from particular.views import particulars_view


app_name = 'core'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('projects/', views.projects, name='projects'),
    path('projects/create/', views.create_project, name='create_project'),
    path('particulars/', particulars_view, name='particulars'),
    path('truck/', views.trucks, name='truck'),
    path('truck/create/', views.trucks, name='truck_create'),
    path('login/', views.login_view, name='login'),
    path("logout/", views.user_logout, name="logout"),
    path('forgot-password/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('forgot-password/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
]