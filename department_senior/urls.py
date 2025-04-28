
from django.urls import path
from . import views

urlpatterns = [
    path('overview_DL/', views.overview_DL, name='overview_DL'), #creating url to view the overview DL
     
    path ('overview_SM/', views.overview_SM, name = 'overview_SM'), #adding a url path to the overview for SM

    path ('dashboard_SM/', views.dashboard_SM, name = 'dashboard_SM'), #adding a url path to the dashbaord for SM

    path ('dashboard_DL/', views.dashboard_DL, name ='dashboard_DL'), #adding a url path to the dashboard for DL

    path('teamprogress_SM/', views.teamprogress_SM, name="teamprogress_SM"), #url to access the SM teamprogress page through the dashboard

    path('teamprogress_DL/', views.teamprogress_DL, name="teamprogress_DL"), #url to access the DL teamprogress page through the dashboard
]

