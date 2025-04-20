from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [    #the migration depends on the authencatication app and 0001_initial.py, 
                        #which means that changes can only be made once the 0001_initial.py runs
        ("authentication", "0001_initial"),
    ]

    operations = [  
        migrations.AlterField(  #will make changes that was applied to the database in this migration
            model_name="profile",   #where the change is happening
            name="role",    #the field that can be modified
            field=models.CharField(
                choices=[    #options of the roles for them to choose as a dropdown in forms
                    ("engineer", "Engineer"),
                    ("team-leader", "Team Leader"),
                    ("department-leader", "Department Leader"),
                    ("senior-manager", "Senior Manager"),
                    ("admin", "Admin"),
                ],
                max_length=50,      #max length for the role string
            ),
        ),
    ]
