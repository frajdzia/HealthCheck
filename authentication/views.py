from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomLoginForm, ForgetPasswordForm, TeamProgressFilterForm
from django.contrib.auth.models import User

def team_progress(request):         #to view the teamprogress_SM.html if the users role is senior manager
    user = request.user             #getting the user
    if user.is_authenticated:       #getting the current user that is logged in
        if hasattr(user, 'profile') and user.profile.role == 'Senior Manager':      #check if users role is 'Senior Manager'
            return render(request, 'authentication/teamprogress_SM.html')           #goes to teamprogress for roles that are Senior Manager
        else:
            return render(request, 'authentication/teamprogress_SM.html')           #goes to teamprogress for roles that are engineers
    else:
        return redirect('login')            #returns to login.html if user is not logged in

def signup_view(request):           #view to handle the users sign up
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST) #populatin the form with the informations that the user input
        
        if form.is_valid():         #check if input form is valid
            user = form.save()      #save the users input form
            messages.success(request, f'Account created for {user.username}!')      #if successful, print the message and the username
            return redirect('dashboard')    #goes to the home page (dashboard) if succesfful
        else:
            return render(request, 'authentication/signup.html', {'form': form})        #redirects to signup.html if fails
    else:
        form = CustomUserCreationForm()         #return the form again

    return render(request, 'authentication/signup.html', {'form': form})

class CustomLoginView(LoginView):       #view to handle the login view with Django's LoginView
    template_name = 'authentication/login.html'         #custom login form specification for the template
    authentication_form = CustomLoginForm               #custom login form specification

    success_url = reverse_lazy('dashboard')             #goes to dashboard if login is successful

def forget_password(request):       #view to handle the forgetpassword.html to reset the password for the user
    if request.method == 'POST':
        form = ForgetPasswordForm(request.POST)     #populate the form with the information that the user input
        if form.is_valid():         #check if the input form is valid
            username = form.cleaned_data['username']                #get username from form
            new_password = form.cleaned_data['new_password']        #get password from form
            
            user = User.objects.get(username=username)      #getting the user from the database
            user.set_password(new_password)                 #setting new password for the current user
            user.save()                                     #saving the changes

            messages.success(request, 'Password reset successful. Please log in with your new password.')   #successful message
            return redirect('login')                        #goes to login after resetting the password
    else:
        form = ForgetPasswordForm()
    
    return render(request, 'authentication/forgetpassword.html', {'form': form})    #redirects to forgetpassword.html if fails


