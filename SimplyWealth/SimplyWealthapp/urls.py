from django.urls import path
from . import views

urlpatterns =[
    path('', views.home, name='home'),
    path('', views.stock_graph, name='stock-graph')
]