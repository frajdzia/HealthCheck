from django.contrib import admin
from .models import UserSelection

@admin.register(UserSelection)
class UserSelectionAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'team', 'created_at')
    search_fields = ('user__username', 'department__name', 'team__team_name')
