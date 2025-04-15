from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Password'}))

    def confirm_login_allowed(self, user):
        # Only allow login if user has a profile (i.e., signed up properly)
        if not hasattr(user, 'profile'):
            raise forms.ValidationError(
                "This account is not properly set up. Please sign up first.",
                code='invalid_login'
            )

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Last Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Username'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Confirm Password'}))
    role = forms.ChoiceField(
        choices=[
            ('engineer', 'Engineer'),
            ('team-leader', 'Team Leader'),
            ('department-leader', 'Department Leader'),
            ('senior-manager', 'Senior Manager'),
            ('admin', 'Admin'),
        ],
        required=True,
        widget=forms.Select(attrs={'class': 'form-input'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()
            # Save the profile with the role
            role = self.cleaned_data['role']
            Profile.objects.create(user=user, role=role)

        return user
    
class ForgetPasswordForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Username'}))
    phoneno = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone number'}))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'New password'}))
    code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Code'}))  # Optional

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')

        if username and not User.objects.filter(username=username).exists():
            raise forms.ValidationError("This user does not exist.")
        return cleaned_data

class TeamProgressFilterForm(forms.Form):
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

    team = forms.ChoiceField(choices=TEAM_CHOICES)
    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES)
    duration = forms.ChoiceField(choices=DURATION_CHOICES)
