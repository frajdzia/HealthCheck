from django.urls import path
from . import views


urlpatterns = [
    path('adminDashboard/', views.admin_dashboard, name='admin_dashboard'),
]
