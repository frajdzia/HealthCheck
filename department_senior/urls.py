
from django.urls import path
from . import views

urlpatterns = [
    path('overview_DL/', views.overview_DL, name='overview_DL'),
     
    path ('overview_SM/', views.overview_SM, name = 'overview_SM'),

    path ('dashboard_SM/', views.dashboard_SM, name = 'dashboard_SM'), 

    path ('dashboard_DL/', views.dashboard_DL, name ='dashboard_DL'),

    path('teamprogress_SM/', views.teamprogress_SM, name="teamprogress_SM"),

    path('teamprogress_DL/', views.teamprogress_DL, name="teamprogress_DL"), 
]

