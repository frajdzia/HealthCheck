from django.urls import include, path
from .import views

urlpatterns =[
    # #URL for team progress DL  page
    path('teamprogress_DL/', views.team_progress, name='team_progress_department_leader'),

    #URL for profile page
    path('profile/', views.profile, name='profile'),
]


