from django.shortcuts import render

def overview_DL (request):
    return render(request, 'department_senior/overview_DL.html')

def overview_SM (request):
    return render (request, 'department_senior/overview_SM.html')

def dashboard_DL(request):
    return render(request, 'department_senior/dashboard_DL.html')

def dashboard_SM (request):
    return render(request, 'department_senior/dashboard_SM.html')

def teamprogress_SM (request):
    return render(request, 'department_senior/teamprogress_SM.html')

