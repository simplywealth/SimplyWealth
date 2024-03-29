from django.urls import path 
from . import views
from .views import line_chart, line_chart_json

urlpatterns = [
    path("", views.index, name='index'),
    path("signup/", views.signup, name='signup'),
    path("login_view/", views.login_view, name='login_view'),
    path('userhome/', views.userhome, name='userhome'),
    path('chart', line_chart, name='line_chart'),
    path('chartJSON', line_chart_json, name='line_chart_json'),
    path('upload-profile-picture/', views.upload_profile_picture, name='upload_profile_picture'),
    path('get_ticker_details', views.get_ticker_details, name='get_ticker_details')
#    path("<str:username>/", views.userhome, name='userhome')
]