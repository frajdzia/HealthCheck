from django.db import models
from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model): #extending the user built in model with Profile
    user = models.OneToOneField(User, on_delete=models.CASCADE) #creating a one-to-one relationship for profile and user
    role = models.CharField(max_length=50, choices=[        #roles for the users to select and settting max characters to 50
        ('engineer', 'Engineer'),
        ('team-leader', 'Team Leader'),
        ('department-leader', 'Department Leader'),
        ('senior-manager', 'Senior Manager'),
    ])  

    def __str__(self):
        return f"{self.user.username} - {self.role}"    #show usernaame and role when profile is printed


