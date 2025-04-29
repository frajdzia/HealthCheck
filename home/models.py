from django.db import models
from django.contrib.auth.models import User
from authentication.models import Profile

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class Team(models.Model):
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    team_name = models.CharField(max_length=255)
    team_leader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.team_name

class UserSelection(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username}'s selection"

class Question(models.Model):
    text = models.CharField(max_length=255)
    category = models.CharField(max_length=100, default='General')
    def __str__(self):
        return self.text

class Card(models.Model):
    TREND_CHOICES = [
        (0, 'Red - Risky, painful, manual, slow'),
        (1, 'Yellow - Difficult but doable'),
        (2, 'Green - Simple, safe, automated'),
    ]
    STATE_CHOICES = [
        ('declining', 'Declining'),
        ('improving', 'Improving'),
        ('stable', 'Stable'),
    ]
    votes = models.IntegerField(default=0)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='cards')
    trend = models.IntegerField(choices=TREND_CHOICES, default=1)
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default='stable')
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True, related_name='cards')
    def __str__(self):
        return f"{self.question.text if self.question else 'No Question'} - {self.team.team_name}"

class Session(models.Model):
    date = models.DateTimeField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='sessions')
    is_finished = models.BooleanField(default=False)
    voting_results = models.JSONField(default=dict)
    def __str__(self):
        return f"{self.team.team_name} - {self.date}"

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='vote_records')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='votes')
    trend = models.IntegerField(choices=Card.TREND_CHOICES)
    state = models.CharField(max_length=20, choices=Card.STATE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user', 'card', 'session')
    def __str__(self):
        return f"{self.user.username} - {self.card.question.text if self.card.question else 'No Question'} - {self.get_trend_display()}"