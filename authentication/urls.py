from django.urls import include, path
from authentication import views as auth_views
from authentication.views import CustomLoginView

urlpatterns =[
    #URL for login page, users will be directed to the login.html when users run the server
    path('', CustomLoginView.as_view(), name='login'),

    #URL for signup page
    path('signup/', auth_views.signup_view, name='signup'),

    #URL for forget password page
    path('forgetpassword/', auth_views.forget_password, name='forgetpassword'),

        #URL for team progress page
    path('teamprogress_SM/', auth_views.team_progress, name="teamprogress"),

    path('progress/', auth_views.progress_redirect, name='progress'),

]