from django.urls import path
from . import views


app_name = "particular"


urlpatterns = [
    path('', views.particular_list, name='particulars'), # Optional: for redirection
    path('index/', views.index, name='index'),
    path('create/', views.create_particular, name='create_particular'),
    path('import/', views.import_from_file, name='import_from_file'),
    path('equipments/create/', views.create_equipment, name='create_equipment'),
]

