from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile #impprting the custom profile model to store tuser information 'role'

class CustomLoginForm(AuthenticationForm):
    #overriding the username and adding the class from style.css with placeholder Username
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Username'}))
    #overriding the password and adding the class from style.css with placeholder Password
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Password'}))

    def confirm_login_allowed(self, user):
        # Only allow login if user has a profile
        if not hasattr(user, 'profile'):
            raise forms.ValidationError(    #show error message if failed to sign up
                "This account is not properly set up. Please sign up first.",
                code='invalid_login'
            )

class CustomUserCreationForm(UserCreationForm):
    #overriding the first name and adding the class from style.css with placeholder First Name
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First Name'}))
    #overriding the last name and adding the class from style.css with placeholder Last Name
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Last Name'}))
    #overriding the email and adding the class from style.css with placeholder Email
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email'}))
    #overriding the username and adding the class from style.css with placeholder Username
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Username'}))
    #overriding the password and adding the class from style.css with placeholder Password
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Password'}))
    #overriding the password confirmation and adding the class from style.css with placeholder Confirm password
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Confirm Password'}))
    role = forms.ChoiceField(       #show the choices for the role
        choices=[
            ('engineer', 'Engineer'),
            ('team-leader', 'Team Leader'),
            ('department-leader', 'Department Leader'),
            ('senior-manager', 'Senior Manager'),
            
        ],
        required=True,
        widget=forms.Select(attrs={'class': 'form-input'}) #adding the custom dropdown
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)       #saving the user object
        user.set_password(self.cleaned_data['password1'])       #setting the password for the user

        if commit:
            user.save()         #adding the user to the database
            role = self.cleaned_data['role']        # Save the profile with the role
            Profile.objects.create(user=user, role=role)        #create a profile which will display the user and the role

        return user
    
class ForgetPasswordForm(forms.Form):
    #overriding the username and adding the class from style.css with placeholder Username
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Username'}))
    #overriding the phoneno and adding the class from style.css with placeholder Phone number
    phoneno = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone number'}))
    #overriding the new_password and adding the class from style.css with placeholder New password
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'New password'}))
    #overriding the code and adding the class from style.css with placeholder code
    code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Code'}))

    def clean(self):
        cleaned_data = super().clean()      #checking to see if username exists in the database
        username = cleaned_data.get('username')

        if username and not User.objects.filter(username=username).exists():        #checking if user exists with the username entered
            raise forms.ValidationError("This user does not exist.")                #if user does not exist, show the error message
        return cleaned_data

class TeamProgressFilterForm(forms.Form):           #creating a drop down list for the teamprogress_SM.html
    TEAM_CHOICES = [
        ('team1', 'Team 1'),
        ('team2', 'Team 2'),
        ('team3', 'Team 3'),
        ('team4', 'Team 4'),
    ]
    DEPARTMENT_CHOICES = [
        ('dept1', 'Department 1'),
        ('dept2', 'Department 2'),
        ('dept3', 'Department 3'),
        ('dept4', 'Department 4'),
    ]
    DURATION_CHOICES = [
        ('1m', '1 Month'),
        ('6m', '6 Months'),
        ('1y', '1 Year'),
    ]
    #creating the forms with the options provided above›
    team = forms.ChoiceField(choices=TEAM_CHOICES)
    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES)
    duration = forms.ChoiceField(choices=DURATION_CHOICES)
