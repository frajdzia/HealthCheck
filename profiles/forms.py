from django import forms
from django.contrib.auth.models import User
from authentication.models import Profile

class UserUpdateForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'New Password'}),
        required=False  # Password is optional
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Last Name'}),
            'username': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email'}),
        }

def save(self, commit=True):
    user = super().save(commit=False)
    new_password = self.cleaned_data.get('password')

    if new_password:
        user.set_password(new_password)  # Securely set password only if provided

    if commit:
        user.save()

    return user