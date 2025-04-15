"""
URL configuration for HealthCheck project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #URL for admin page
    path('admin/', admin.site.urls, name='admin'),
    
    # URL for home page
    path('', include('home.urls')),

    path('', include('profiles.urls')),
]

# Serve static files during development
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
