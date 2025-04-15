from django.db import models
from django.contrib.auth.models import User as DjangoUser

class Team(models.Model):
    team_name = models.CharField(max_length=255)
    team_leader = models.CharField(max_length=255)

    def __str__(self):
        return self.team_name

class Admin(models.Model):
    user = models.ForeignKey('AppUser', on_delete=models.CASCADE, related_name='admin_roles')  # Added related_name
    admin_id = models.CharField(max_length=255, primary_key=True)

    def __str__(self):
        return self.admin_id
    
class AppUser(models.Model):
    django_user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE)
    role = models.CharField(max_length=255)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
    card = models.ForeignKey('Card', on_delete=models.CASCADE, null=True)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE, null=True)
    has_completed_form = models.BooleanField(default=False)  # New field

    def __str__(self):
        return self.django_user.username
    
class Card(models.Model):
    votes = models.FloatField(null=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    trend = models.IntegerField()
    state = models.IntegerField()
    comments = models.TextField()

    def __str__(self):
        return f"Card {self.id}"

class Session(models.Model):
    date = models.DateTimeField(null=True)
    update_progress = models.TextField()
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"Session {self.id}"