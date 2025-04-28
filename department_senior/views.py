from django.shortcuts import render

def overview_DL (request):
    return render(request, 'department_senior/overview_DL.html') #view the overview of department leader (within their dashabord)

def overview_SM (request):
    return render (request, 'department_senior/overview_SM.html') #view the the overview of senior manager(within thier dashbaord)

def dashboard_DL(request):
    return render(request, 'department_senior/dashboard_DL.html') #view the dashbaord for department leader

def dashboard_SM (request):
    return render(request, 'department_senior/dashboard_SM.html') #view the dashbaord for senior manager

def teamprogress_SM (request):
    return render(request, 'department_senior/teamprogress_SM.html') #to view the the team progressSM page within the dashbaord

def teamprogress_DL (request):
    return render(request, 'profiles/teamprogress_DL.html') #created url routing connection between teamprogressDL within profiles app
