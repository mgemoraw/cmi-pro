from django.urls import path
from . import views


app_name = "particular"


urlpatterns = [
    path('', views.index, name='particulars'), # Optional: for redirection
    path('list/', views.particular_list, name='particulars_list'),
    path('create/', views.create_particular, name='create_particular'),
    path('create_project/', views.create_project_sector, name="create_project"),
    path('import/', views.import_from_file, name='import_from_file'),
    path('equipments/create/', views.create_equipment, name='create_equipment'),
]

