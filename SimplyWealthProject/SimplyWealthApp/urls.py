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
    path('buy_stock', views.buy_stock, name='buy_stock'),
    path('get_ticker_details', views.get_ticker_details, name='get_ticker_details'),
    path('get_stock_units', views.get_stock_units, name='get_stock_units'),
    path('sell_stock', views.sell_stock, name='sell_stock'),
    path('logout_view',views.logout_view, name='logout_view')
    
#    path("<str:username>/", views.userhome, name='userhome')
]