from django.shortcuts import render
from home.models import Department, Team  #  you import the models


# view the overview of department leader (within their dashboard)
def overview_DL(request):
    departments = Department.objects.all()
    selected_department_id = request.GET.get('department')
    selected_department = None
    best_team_name = None
    best_team_performance = None
    worst_team_name = None
    worst_team_performance = None

    # if the department is selected
    if selected_department_id:
        try:
            selected_department = Department.objects.get(id=int(selected_department_id))  # force int!
            teams = Team.objects.filter(department=selected_department)[:2]  # first 2 teams

            if teams:

                performances = {team.team_name: 87 - i * 23 for i, team in enumerate(teams)}
                sorted_performance = sorted(performances.items(), key=lambda x: x[1], reverse=True)

                best_team_name, best_team_performance = sorted_performance[0]
                if len(sorted_performance) > 1:
                    worst_team_name, worst_team_performance = sorted_performance[-1]
                else:
                    worst_team_name, worst_team_performance = best_team_name, best_team_performance

        except (Department.DoesNotExist, ValueError):
            selected_department = None

    return render(request, 'department_senior/overview_DL.html', {
        'departments': departments,
        'selected_department': selected_department,
        'best_team_name': best_team_name,
        'best_team_performance': best_team_performance,
        'worst_team_name': worst_team_name,
        'worst_team_performance': worst_team_performance,
    })


# view the overview of senior manager (within their dashboard)
def overview_SM(request):
    departments = Department.objects.all()
    selected_department_id = request.GET.get('department')
    selected_department = None
    best_team_name = None
    best_team_performance = None
    worst_team_name = None
    worst_team_performance = None

    # if the department is selected
    if selected_department_id:
        try:
            selected_department = Department.objects.get(id=int(selected_department_id))  # force int!
            teams = Team.objects.filter(department=selected_department)[:2]  # first 2 teams

            if teams:
                performances = {team.team_name: 80 - i * 15 for i, team in enumerate(teams)}
                sorted_performance = sorted(performances.items(), key=lambda x: x[1], reverse=True)

                best_team_name, best_team_performance = sorted_performance[0]
                if len(sorted_performance) > 1:
                    worst_team_name, worst_team_performance = sorted_performance[-1]
                else:
                    worst_team_name, worst_team_performance = best_team_name, best_team_performance

        except (Department.DoesNotExist, ValueError):
            selected_department = None

    return render(request, 'department_senior/overview_SM.html', {
        'departments': departments,
        'selected_department': selected_department,
        'best_team_name': best_team_name,
        'best_team_performance': best_team_performance,
        'worst_team_name': worst_team_name,
        'worst_team_performance': worst_team_performance,
    })
    
def dashboard_DL(request):
    return render(request, 'department_senior/dashboard_DL.html') #view the dashbaord for department leader

def dashboard_SM(request):
    return render(request, 'department_senior/dashboard_SM.html') #view the dashbaord for senior manager

def teamprogress_SM(request):
    return render(request, 'department_senior/teamprogress_SM.html') #to view the the team progressSM page within the dashbaord

def teamprogress_DL(request):
    return render(request, 'profiles/teamprogress_DL.html') #created url routing connection between teamprogressDL within profiles app
