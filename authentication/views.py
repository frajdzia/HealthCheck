from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomLoginForm, ForgetPasswordForm
from home.forms import TeamProgressFilterForm
from django.contrib.auth.models import User
from home.views import team_progress_summary  # Import the reusable function
from django.http import HttpResponseForbidden


def team_progress(request):         #to view the teamprogress_SM.html if the users role is senior manager
    user = request.user             #getting the user
    print(f"team_progress: user={user}, is_authenticated={user.is_authenticated}")
    if user.is_authenticated:       #getting the current user that is logged in
        if hasattr(user, 'profile'):
            role = user.profile.role
            print(f"team_progress: role={role}")
            if role == 'senior-manager':      #check if users role is 'Senior Manager'
                # Use the reusable function
                form = TeamProgressFilterForm(user=request.user, data=request.POST or None)
                print(f"team_progress: form created, bound={form.is_bound}")
                team_summary, selected_date, form, template_name = team_progress_summary(
                    user=request.user, role='senior-manager', form=form
                )
                print(f"team_progress: team_summary={team_summary}, selected_date={selected_date}, template_name={template_name}")
                return render(request, template_name, {
                    'form': form,
                    'team_summary': team_summary,
                    'selected_date': selected_date,
                })           #goes to teamprogress for roles that are Senior Manager
            elif role == 'engineer':
                return redirect('summary')  # engineers go to summary
            else:
                return redirect('teamprogress_DL')  # department leaders go to their page
        else:
            messages.error(request, "User profile not found.")
            print("team_progress: User profile not found")
            return redirect('login')
    else:
        print("team_progress: User not authenticated")
        return redirect('login')            #returns to login.html if user is not logged in

    
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST) #populatin the form with the informations that the user input
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get('role')
            if hasattr(user, 'profile'):
                user.profile.role = role
                user.profile.save()
            messages.success(request, f'Account created for {user.username}! Please log in.') #if successful print message and the username
            return redirect('login')  # Redirect to login page after successful signup
        else:
            return render(request, 'authentication/signup.html', {'form': form})
    else:
        form = CustomUserCreationForm()

    return render(request, 'authentication/signup.html', {'form': form})

class CustomLoginView(LoginView):       #view to handle the login view with Django's LoginView
    template_name = 'authentication/login.html'         #custom login form specification for the template
    authentication_form = CustomLoginForm               #custom login form specification
    print("Authentication form: ", authentication_form)
    
    def get_success_url(self):  #codes from line 49 to line 57 is implemented by Sham
        
        if self.request.user.profile.role == 'department-leader':
            
            return reverse_lazy('dashboard_DL')
        elif self.request.user.profile.role == 'senior-manager':
            return reverse_lazy('dashboard_SM')
        else:
            return reverse_lazy('dashboard')             #goes to dashboard if login is successful

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



def progress_redirect(request): #done by sham line 81 - 93
    user = request.user
    if hasattr(user, 'profile'):
        role = user.profile.role
        if role in ['engineer', 'team-leader']:
            return redirect('summary')  # home/urls.py
        elif role == 'department-leader':
            return redirect('teamprogress_DL')  # profiles/urls.py 
        elif role == 'senior-manager':
            return redirect('teamprogress_SM')  # authentication/urls.py
        else:
            return HttpResponseForbidden("Role not allowed.")
    return redirect('login')
