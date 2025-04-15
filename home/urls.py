from django.urls import path
from .views import dashboard, voting, summary

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('voting/<str:team_name>/', voting, name='voting'),
    path('summary/', summary, name='summary'),
]