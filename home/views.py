from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from home.models import AppUser, Card, Team

@login_required
def dashboard(request):
    teams = Team.objects.all()
    roles = ['Developer', 'Manager', 'Tester']
    
    # Fallback: Create AppUser if it doesn't exist
    user, created = AppUser.objects.get_or_create(
        django_user=request.user,
        defaults={
            'role': 'Developer',  # Temporary default
            'has_completed_form': False
        }
    )
    
    # Ensure at least one Team exists for testing
    if not teams.exists():
        Team.objects.create(team_name="Default Team", team_leader="Test Leader")
        teams = Team.objects.all()
    
    if user.has_completed_form and user.team:
        return redirect('voting', team_name=user.team.team_name)
    
    if request.method == 'POST':
        role = request.POST.get('role')
        team_name = request.POST.get('team')
        if role and team_name:
            try:
                user.role = role
                user.team = Team.objects.get(team_name=team_name)
                user.has_completed_form = True
                user.save()
                return redirect('voting', team_name=team_name)
            except Team.DoesNotExist:
                pass  # Handle invalid team input
    if request.method == 'GET':
        if request.user.profile.role == 'department-leader':
            return redirect('dashboard_DL')
        elif request.user.profile.role == 'senior-manager':
            return redirect('dashboard_SM')
        else:
            return redirect('dashboard')
    return render(request, 'home/home.html', {'teams': teams, 'roles': roles})


# , {'teams': teams, 'roles': roles}
@login_required
def voting(request, team_name):
    try:
        team = Team.objects.get(team_name=team_name)
        user = AppUser.objects.get(django_user=request.user)
    except (Team.DoesNotExist, AppUser.DoesNotExist):
        return redirect('dashboard')  # Redirect if data is missing
    cards = Card.objects.filter(team=team)
    if request.method == 'POST':
        state = request.POST.get('state')
        card_id = request.POST.get('card_id')
        try:
            card = Card.objects.get(id=card_id)
            card.state = int(state)
            card.votes = (card.votes or 0) + 1
            card.save()
            user.has_completed_form = True
            user.save()
            return redirect('summary')
        except Card.DoesNotExist:
            pass
    return render(request, 'home/voting.html', {'team': team, 'cards': cards})

# @login_required
def summary(request):
    return render(request, 'home/summary.html')