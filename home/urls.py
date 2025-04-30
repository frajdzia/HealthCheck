from django.urls import path
from . import views

urlpatterns = [
    # dashboard page for engineer & team leader
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # voting page
    path('voting/<int:session_id>/', views.voting, name='voting'),
    
    # summary/(engineer & team leader) progress page
    path('summary/', views.summary, name='summary'),
    
    # teams selection based on department
    path('get-teams/', views.get_teams, name='get_teams'),

    # check if user has asigned team & department
    path('home-vote-view/', views.home_vote_view, name='home_vote_view'),
]