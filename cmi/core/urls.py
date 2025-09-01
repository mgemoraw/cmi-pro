from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from particular.views import particular_list


app_name = 'core'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('settings/', views.settings_view, name='settings'),
    path('projects/', views.projects, name='projects'),
    path('projects/create/', views.create_project, name='create_project'),
    path('projects/import/', views.import_project_data, name="import-project-data"),
    path('projects/download/', views.download_template, name='download-template'),
    path('particulars/', views.particular_dashboard, name='particulars'),
    path('instances/', views.instance_dashboard, name='instances'),
    path('instances/create/', views.create_instance_view, name='create-instance'),
    path('work-items/', views.work_items, name='work-items'),
    path('truck/', views.trucks, name='truck'),
    path('truck/create/', views.trucks, name='truck_create'),
    path('dozer/', views.dozers, name='dozer'),
    path('dozer/create/', views.create_dozer, name='dozer-create'),
    path('excavator/', views.excavators, name='excavator'),
    path('excavator/create/', views.create_dozer, name='excavator-create'),
    path('labor/', views.labors, name='labor'),
    path('labor/create/', views.create_labor, name='labor-create'),
    path('work-sampling/', views.work_sampling, name='work-sampling'),
    path('work-sampling/create/', views.create_ws, name='work-sampling-create'),
    path('login/', views.login_view, name='user-login'),
    path("logout/", views.user_logout, name="user-logout"),
    path('forgot-password/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('forgot-password/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
]