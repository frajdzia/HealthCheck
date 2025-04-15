from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomLoginForm, ForgetPasswordForm, TeamProgressFilterForm
from django.contrib.auth.models import User

def team_progress(request):
    user = request.user
    if user.is_authenticated:
        if hasattr(user, 'profile') and user.profile.role == 'Senior Manager':
            return render(request, 'authentication/teamprogress_SM.html')
        else:
            return render(request, 'authentication/teamprogress_TM.html')
    else:
        return redirect('login')

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created for {user.username}!')
            return redirect('home')  # Make sure 'home' is defined in your URLs
        else:
            return render(request, 'authentication/signup.html', {'form': form})
    else:
        form = CustomUserCreationForm()

    return render(request, 'authentication/signup.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'authentication/login.html'
    authentication_form = CustomLoginForm

    success_url = reverse_lazy('home')

def forget_password(request):
    if request.method == 'POST':
        form = ForgetPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            new_password = form.cleaned_data['new_password']
            
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()

            messages.success(request, 'Password reset successful. Please log in with your new password.')
            return redirect('login')
    else:
        form = ForgetPasswordForm()
    
    return render(request, 'authentication/forgetpassword.html', {'form': form})

def team_progress(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    form = TeamProgressFilterForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        # handle form submission logic here
        pass

    if hasattr(user, 'role') and user.role == 'SM':
        return render(request, 'authentication/teamprogress_SM.html', {'form': form})
    else:
        return render(request, 'authentication/teamprogress_SM.html', {'form': form})

