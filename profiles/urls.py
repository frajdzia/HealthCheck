from django.urls import include, path
from .import views

urlpatterns =[
    # #URL for admin profile page
    # path('adminProfile/', views.adminProfile, name='adminprofile'),

    #URL for profile page
    path('profile/', views.profile, name='profile'),
]


