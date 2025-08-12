from django.urls import path
from . import views


app_name = "particular"


urlpatterns = [
    path('index/', views.index, name='index'),
]