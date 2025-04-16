from django.shortcuts import render

def overview(request):
    return render(request, 'department_senior/overview.html')

def dashboard(request):
    return render(request, 'department_senior/dashboards.html')


