
from os import pathconf_names

from django.urls import path

from expense import views

app_name = 'expense'
urlpatterns =[
    path('', views.index, name='index'),
]