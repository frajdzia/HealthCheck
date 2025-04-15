from django.db import models
from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    role = models.CharField(max_length=50, choices=[
        ('engineer', 'Engineer'),
        ('team-leader', 'Team Leader'),
        ('department-leader', 'Department Leader'),
        ('senior-manager', 'Senior Manager'),
        ('admin', 'Admin'),
    ])  

    def __str__(self):
        return f"{self.user.username} - {self.role}"


