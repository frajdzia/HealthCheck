from django.shortcuts import render
from home.models import Team, Card, Session
from authentication.models import Profile
# Create your views here.

def admin_dashboard(request):
    context = {
        "team_count": Team.objects.count(),
        "card_count": Card.objects.count(),
        "session_count": Session.objects.count(),
        "user_count": Profile.objects.count(),
    }
    return render(request, 'adminhealthcheck/adminDashboard.html', context)
