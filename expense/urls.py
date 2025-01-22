
from os import pathconf_names

from django.urls import path

from expense import views

app_name = 'expense'

urlpatterns = [
    path('', views.index, name='index'),
    path('fetch-data-overview/', views.fetch_data_overview, name='fetch_data_overview'),
    path('delete-entry/', views.delete_entry, name='delete_entry'),
    path('draw-graph/', views.draw_graph, name='draw_graph'),
]
