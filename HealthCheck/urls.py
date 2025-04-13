"""
URL configuration for HealthCheck project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from home import views

urlpatterns = [
    #URL for admin page
    path('admin/', admin.site.urls, name='admin'),
    
    # URL for home page
    path('', views.home, name='home'),

    path('', include('profiles.urls')),
]

# Serve static files during development
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
