"""
URL configuration for HealthCheck project.
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from home import views
from profiles import views as profile_views

urlpatterns = [
    #URL for admin page
    path('admin/', admin.site.urls, name='admin'),
    
    # URL for home page
    path('', views.home, name='home'),

    #URL for admin profile page
    path('adminProfile/', profile_views.adminProfile, name='admin profile'),

    #URL for profile page
    path('profile/', profile_views.profile, name='profile'),
]

# Serve static files during development
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
