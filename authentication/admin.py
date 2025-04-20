
from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin): #to create a custome profile admin so that Profile will appear in the Django admin panel
    list_display = ('user', 'role') #specifies the fields needed for the Profile so that it will display the user and the role of the user

admin.site.register(Profile, ProfileAdmin)  #registers the Profile with the admin site by using the ProfileAdmin class
