from django.urls import path 
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("signup/", views.signup, name='signup'),
    path("<str:username>", views.userhome, name='userhome')
]