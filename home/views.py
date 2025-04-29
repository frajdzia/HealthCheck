from collections import defaultdict
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .models import Team, Question, Card, Session, Vote, Department, UserSelection
from authentication.models import Profile
from django.contrib import messages
from django.db.models import Count
from django.db.models import F
from django.utils import timezone

@login_required
def home_vote_view(request):
    try:
        user_selection = UserSelection.objects.get(user=request.user)
        if user_selection.department and user_selection.team:
            profile = Profile.objects.get(user=request.user)
            context = {
                'has_selection': True,
                'department': user_selection.department,
                'team': user_selection.team,
                'role': profile.role,
            }
            return render(request, 'voting.html', context)
    except UserSelection.DoesNotExist:
        pass

    departments = Department.objects.all()
    return render(request, 'voting.html', {
        'departments': departments,
        'has_selection': False
    })

def get_teams(request):
    department_id = request.GET.get('department_id')
    teams = Team.objects.filter(department_id=department_id).values('id', 'team_name')
    return JsonResponse(list(teams), safe=False)

@login_required
def dashboard(request):
    profile = Profile.objects.get(user=request.user)
    user_role = profile.role

    try:
        user_selection = UserSelection.objects.get(user=request.user)
        has_selection = user_selection.department is not None and user_selection.team is not None
    except UserSelection.DoesNotExist:
        user_selection = None
        has_selection = False

    departments = Department.objects.all()

    if request.method == 'POST' and has_selection:
        session, _ = Session.objects.get_or_create(
            team=user_selection.team,
            date=timezone.now(),
            defaults={'is_finished': False}
        )
        return redirect('voting', session_id=session.id)

    if request.method == 'POST' and not has_selection:
        dept_id = request.POST.get('department')
        team_id = request.POST.get('team')

        if dept_id and team_id:
            try:
                department = Department.objects.get(id=dept_id)
                team = Team.objects.get(id=team_id)

                if not user_selection:
                    user_selection = UserSelection.objects.create(user=request.user, department=department, team=team)
                else:
                    user_selection.department = department
                    user_selection.team = team
                    user_selection.save()

                session, _ = Session.objects.get_or_create(
                    team=team,
                    date=timezone.now(),
                    defaults={'is_finished': False}
                )

                messages.success(request, "Your department and team have been successfully selected.")
                return redirect('voting', session_id=session.id)

            except (Department.DoesNotExist, Team.DoesNotExist):
                messages.error(request, "Invalid department or team.")
        else:
            messages.error(request, "Please select both department and team.")

    return render(request, 'home/home.html', {
        'departments': departments,
        'has_selection': has_selection,
        'department': user_selection.department if user_selection else None,
        'team': user_selection.team if user_selection else None,
        'user_role': user_role,
    })

@login_required
def voting(request, session_id):
    profile = Profile.objects.get(user=request.user)
    if profile.role not in ['engineer', 'team-leader']:
        messages.error(request, "You are not authorized to vote.")
        return redirect('dashboard')
    
    try:
        session = Session.objects.get(id=session_id, is_finished=False)
        team = session.team
    except Session.DoesNotExist:
        messages.error(request, "Session not found or already finished.")
        return redirect('dashboard')
    
    questions = Question.objects.all()
    cards = []
    for question in questions:
        card, _ = Card.objects.get_or_create(
            question=question,
            team=team,
            defaults={
                'trend': 1,
                'state': 'stable',
            }
        )
        cards.append(card)
    
    if request.method == 'POST':
        print("POST data:", dict(request.POST))
        results = {}
        processed_cards = 0
        expected_cards = len(cards)
        card_ids = {card.id for card in cards}
        
        for card_id in card_ids:
            try:
                card_id_str = str(card_id)
                # Handle duplicate POST data by taking the first value
                trend = request.POST.getlist(f'responses[{card_id_str}][trend]')[0] if request.POST.getlist(f'responses[{card_id_str}][trend]') else None
                state = request.POST.getlist(f'responses[{card_id_str}][state]')[0] if request.POST.getlist(f'responses[{card_id_str}][state]') else None
                print(f"Processing card {card_id}: trend={trend}, state={state}")
                
                if not trend or not state or trend not in ['0', '1', '2'] or state not in dict(Card.STATE_CHOICES):
                    print(f"Invalid or missing data for card {card_id}: trend={trend}, state={state}")
                    continue
                
                card = Card.objects.get(id=card_id, team=team)
                # Ensure unique vote per user, card, session
                Vote.objects.update_or_create(
                    user=request.user,
                    card=card,
                    session=session,
                    defaults={'trend': int(trend), 'state': state}
                )
                results[str(card.question.id)] = {'trend': int(trend), 'state': state}
                processed_cards += 1
                print(f"Saved vote for card {card_id}")
            except (Card.DoesNotExist, ValueError, IndexError) as e:
                print(f"Error processing card {card_id}: {e}")
                continue
        
        session.voting_results = {
            'votes': list(Vote.objects.filter(session=session).values(
                'user__username', 'card__question__text', 'trend', 'state'
            ))
        }
        session.is_finished = processed_cards == expected_cards
        session.save()
        print(f"Session {session.id} finished: {session.is_finished}, results: {session.voting_results}, processed: {processed_cards}/{expected_cards}")
        if session.is_finished:
            messages.success(request, "Votes submitted successfully.")
        else:
            messages.warning(request, f"Only {processed_cards} of {expected_cards} votes processed. Please ensure all questions are answered.")
        return redirect('summary')
    
    return render(request, 'home/voting.html', {
        'team': team,
        'cards': cards,
        'trend_choices': Card.TREND_CHOICES,
    })

@login_required
def summary(request):
    profile = Profile.objects.get(user=request.user)
    role = profile.role
    username = profile.user.username

    # Global summary without filtering by date
    today = timezone.now().date()

    # If a specific date is chosen, use that for user-specific votes only
    selected_date = request.GET.get('date', str(today))
    try:
        selected_date = timezone.datetime.strptime(selected_date, "%Y-%m-%d").date()
    except ValueError:
        selected_date = today

    # Filtering user votes based on selected date (only for user-specific votes)
    user_votes = Vote.objects.filter(
        user=request.user,
        created_at__date=selected_date  # Filter by date for user-specific votes
    ).select_related('card__question', 'session').order_by('-created_at')

    # Optionally: Get the user's selected department and team
    try:
        user_selection = UserSelection.objects.get(user=request.user)
        selected_department = user_selection.department
        selected_team = user_selection.team
    except UserSelection.DoesNotExist:
        selected_department = None
        selected_team = None

    # Handle merged results for the team-leader and all their users' votes
    merged_results = defaultdict(lambda: {
        'question': '',
        'red_count': 0,
        'yellow_count': 0,
        'green_count': 0,
        'state_counts': defaultdict(int),
        'department_name': '',
        'team_name': '',
    })

    def get_trend_color(trend):
        return {0: "Red", 1: "Yellow", 2: "Green"}.get(trend, "Unknown")

    sessions = []

    if role == 'team-leader':
        if selected_team:
            # Show sessions for the team they selected via UserSelection
            sessions = Session.objects.filter(team=selected_team, is_finished=True)
        else:
            sessions = Session.objects.none()
    elif role in ['department-leader', 'senior-manager'] or request.user.is_superuser:
        if selected_department:
            sessions = Session.objects.filter(team__department=selected_department, is_finished=True)
        else:
            sessions = Session.objects.filter(is_finished=True)

    print("Role:", role)
    print("Selected dept:", selected_department)
    print("Sessions found:", sessions.count())

    for session in sessions:
        team = session.team
        votes = Vote.objects.filter(session=session).select_related('card__question', 'card__team')
        print(f"Session ID {session.id} for team {team}")
        print(f"  Votes in this session: {votes.count()}")

        for vote in votes:
            question_text = vote.card.question.text
            key = question_text
            merged_results[key]['question'] = question_text
            merged_results[key]['department_name'] = team.department.name if team.department else 'No Department'
            merged_results[key]['team_name'] = team.team_name
            if vote.trend == 0:
                merged_results[key]['red_count'] += 1
            elif vote.trend == 1:
                merged_results[key]['yellow_count'] += 1
            elif vote.trend == 2:
                merged_results[key]['green_count'] += 1
            merged_results[key]['state_counts'][vote.state] += 1

    # Final processing to prepare results for template
    session_results = []
    for data in merged_results.values():
        state = max(data['state_counts'].items(), key=lambda x: x[1])[0] if data['state_counts'] else 'stable'
        trend_counts = {
            0: data['red_count'],
            1: data['yellow_count'],
            2: data['green_count']
        }
        most_common_trend = max(trend_counts.items(), key=lambda x: x[1])[0]
        data.update({
            'trend': most_common_trend,
            'trend_color': get_trend_color(most_common_trend),
            'state': state,
        })
        session_results.append(data)

    # Formatting user votes with the time (Only for the selected date)
    formatted_votes = []
    for vote in user_votes:
        formatted_vote = {
            'question': vote.card.question.text,
            'trend': vote.trend,
            'state': vote.state,
            'time': vote.created_at.strftime("%H:%M")
        }
        formatted_votes.append(formatted_vote)

    return render(request, 'home/summary.html', {
        'session_results': session_results,
        'user_votes': formatted_votes,
        'user_role': role,
        'username': username,
        'selected_department': selected_department,
        'selected_team': selected_team,
        'selected_date': selected_date,
    })
