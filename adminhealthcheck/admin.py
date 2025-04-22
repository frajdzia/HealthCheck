from django.contrib import admin
from home.models import Team, Card, Session, AppUser, Admin
#from authentication.models import Profile
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_name', 'team_leader')
    search_fields = ('team_name',)

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('id', 'team', 'trend', 'state')
    search_fields = ('team__team_name',)

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date')
    search_fields = ('user__django_user__username',)

@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    list_display = ('django_user', 'role', 'team', 'card', 'admin', 'has_completed_form')
    list_filter = ('role', 'team')
    search_fields = ('django_user__username',)

@admin.register(Admin)
class AdminModelAdmin(admin.ModelAdmin):
    list_display = ('admin_id', 'user')
#commented it out since it already registered in the authentication app
#admin.site.register(Profile)


#username Admin
#password Adminforwork
#email admin@sky.com
