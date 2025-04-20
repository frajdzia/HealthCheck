from django.apps import AppConfig


class AuthenticationConfig(AppConfig): #creating a configuration class for the aunthentication app while inheriting from the AppConfig
    default_auto_field = "django.db.models.BigAutoField" #creating a primary key where it increments for every new user
    name = "authentication" #name of the app called 'authentication'
