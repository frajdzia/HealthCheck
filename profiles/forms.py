from django import forms
from django.contrib.auth.models import User
from authentication.models import Profile
from django.contrib.auth.forms import UserChangeForm

from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

class UserUpdateForm(UserChangeForm):
    # custom form for users editing their own profile details
    class Meta:
        model = User
        # fields that are editable through form
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email'}),
            'username': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Username'}),
        }

    # Disable password field (no change on initial load)
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'New Password'}),
        required=False
    )
    
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        # Disable all fields except 'role' on initial load
        for field in self.fields.values():
            if field.widget.attrs.get('id') != 'role':
                field.widget.attrs['disabled'] = 'disabled'

class TeamProgressFilterForm(forms.Form):   
    # filter form for team progress dashboard
    TEAM_CHOICES = [
        ('team1', 'Team 1'),
        ('team2', 'Team 2'),
        ('team3', 'Team 3'),
        ('team4', 'Team 4'),
    ]
    DURATION_CHOICES = [
        ('1m', '1 Month'),
        ('6m', '6 Months'),
        ('1y', '1 Year'),
    ]
    team = forms.ChoiceField(choices=TEAM_CHOICES)
    duration = forms.ChoiceField(choices=DURATION_CHOICES)