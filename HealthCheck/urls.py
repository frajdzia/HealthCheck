""" URL configuration for HealthCheck project. """
from django.contrib import admin
from django.urls import path, include
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from home import views

urlpatterns = [
    #URL for admin page
    path('admin/', admin.site.urls, name='admin'),
    
    # URL for home page
    path('dashboard/', views.dashboard, name='dashboard'),

    path('', include('authentication.urls')),

<<<<<<< HEAD
    
    path('', include('department_senior.urls')),
    


    path('', include('profiles.urls'))

=======
    path('', include('profiles.urls'))
>>>>>>> 2994efd0d86c1ddea79b6554c49a6165bc1a3b74
]

# Serve static files during development
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)