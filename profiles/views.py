from django.shortcuts import render

def adminProfile(request):
    return render(request, 'adminProfile.html')

def profile(request):
    return render(request, 'profile.html')