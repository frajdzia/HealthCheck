from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, logout
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm

# displayes profile form and handles edits 
# if user changes sensitive fields (username or password), they're logged out and must re-authenticate 
def profile(request):
    if request.method == 'POST': 
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            if form.has_changed():
                changed_fields = form.changed_data
                form.save()
                
                # checks whether user has changed username or password, if so then logs out user due to security reasons
                if 'username' in changed_fields or 'password' in changed_fields:
                    return redirect('login') 
                else: 
                    messages.success(request, "Changes made successfully.")
                    return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'profiles/profile.html', {'form': form})

# DL are redirected to role specific dashbaord page 
def team_progress(request):
    user = request.user
    if user.is_authenticated:
        if hasattr(user, 'profile') and user.profile.role == 'department-leader':
            return render(request, 'profiles/teamprogress_DL.html')
        else:
            return render(request, 'profiles/teamprogress_SM.html')
    else:
        return redirect('login')

