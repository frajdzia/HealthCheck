from django.contrib import admin
from home.models import Team, Question, Card, Session, Vote

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_name', 'team_leader')
    search_fields = ('team_name',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text',)
    search_fields = ('text',)

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('question', 'team', 'trend', 'state', 'votes')
    search_fields = ('team__team_name', 'question__text')

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('team', 'date', 'is_finished')
    search_fields = ('team__team_name',)

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'card', 'session', 'trend', 'state')
    search_fields = ('user__username', 'card__question__text')