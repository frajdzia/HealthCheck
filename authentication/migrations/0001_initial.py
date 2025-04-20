from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration): #defining the schema migrations for the database

    initial = True #the first migration in the authentication app

    dependencies = [
        #migration depends on the user model
        #user model is defined in the settings.AUTH_USER_MODEL
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        #contains all the database operations
        migrations.CreateModel(
            name="Profile", #name for the model created
            fields=[
                #making the ID to be the primary key
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,  #auto create and increment the ID
                        primary_key=True,   #making the ID field to be the primary key
                        serialize=False,    #to not include during serializing
                        verbose_name="ID",  #make it to human-readable format
                    ),
                ),
                (
                    #making a role for each user from the options that they select
                    "role",
                    models.CharField(
                        choices=[   #the options of the roles for them to choose as a dropdown in forms
                            ("engineer", "Engineer"),
                            ("team-leader", "Team Leader"),
                            ("department-leader", "Department Leader"),
                            ("senior-manager", "Senior Manager"),
                            ("admin", "Admin"),
                        ],
                        max_length=30,  #maximum length for the string
                    ),
                ),
                (
                    "user",
                    #one-to-one relationship to link the profile to a user
                    #each user can only have one profile, vise versa
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,    #to delete the profile is user is deleted
                        to=settings.AUTH_USER_MODEL,    #link to user model which specified in settings
                    ),
                ),
            ],
        ),
    ]
