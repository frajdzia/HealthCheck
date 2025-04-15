from django.shortcuts import render

def adminProfile(request):
    return render(request, 'profiles/adminProfile.html')

def profile(request):
    return render(request, 'profiles/profile.html')