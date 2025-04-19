from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, logout
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm

def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Changes made successfully.")
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'profiles/profile.html', {'form': form})