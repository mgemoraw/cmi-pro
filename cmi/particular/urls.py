from django.urls import path
from . import views


app_name = "particular"


urlpatterns = [
    path('index/', views.index, name='index'),
    path('', views.particular_list, name='particular_list'), # Optional: for redirection
    path('particulars/create/', views.create_particular, name='create_particular'),
]

