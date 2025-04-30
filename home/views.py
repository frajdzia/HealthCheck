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
from .utils import save_unique_vote, get_team_summary
from datetime import timedelta
from home.forms import TeamProgressFilterForm

# Reusable function to fetch team progress summaries based on role
def team_progress_summary(user, role, form=None, selected_date=None):
    """
    Fetches team voting summaries based on user role and filters.
    Args:
        user: The authenticated user.
        role: The user's role ('team-leader', 'department-leader', 'senior-manager').
        form: TeamProgressFilterForm instance for filtering (optional).
        selected_date: The date to filter votes (default: today).
    Returns:
        Tuple of (team_summary, selected_date, form, template_name).
    """
    print(f"team_progress_summary: user={user.username}, role={role}, selected_date={selected_date}")
    if not selected_date:
        selected_date = timezone.now().date()
        print(f"team_progress_summary: defaulted selected_date to {selected_date}")

    # Initialize form if not provided, pass the user to the form
    if form is None:
        form = TeamProgressFilterForm(user=user)
        print("team_progress_summary: form initialized")

    # Fetch team summary based on role
    team_summary = get_team_summary(user, role, selected_date)
    print(f"team_progress_summary: team_summary={team_summary}")

    # Apply filters based on role and form input
    if form.is_bound and form.is_valid():
        print("team_progress_summary: form is bound and valid")
        team = form.cleaned_data.get('team')
        department = form.cleaned_data.get('department')
        duration = form.cleaned_data.get('duration')
        date = form.cleaned_data.get('date')
        print(f"team_progress_summary: form data - team={team}, department={department}, duration={duration}, date={date}")

        # Apply date filter if provided
        if date:
            selected_date = date
            team_summary = get_team_summary(user, role, selected_date)
            print(f"team_progress_summary: applied date filter, new selected_date={selected_date}, team_summary={team_summary}")

        # Apply duration filter (takes precedence over date if both are provided)
        if duration:
            days = int(duration)
            date_from = timezone.now().date() - timedelta(days=days)
            selected_date = date_from
            team_summary = get_team_summary(user, role, selected_date)
            print(f"team_progress_summary: applied duration filter, new selected_date={selected_date}, team_summary={team_summary}")

        # Apply team and department filters
        if team or department:
            filtered_summary = []
            for result in team_summary:
                # Skip if team filter is set and doesn't match (case-insensitive)
                if team and result['team_name'].strip().lower() != team.team_name.strip().lower():
                    print(f"team_progress_summary: Excluded team - result.team_name={result['team_name']}, filter.team_name={team.team_name}")
                    continue
                # Skip if department filter is set and doesn't match (case-insensitive)
                if department and result['department_name'].strip().lower() != department.name.strip().lower():
                    print(f"team_progress_summary: Excluded department - result.department_name={result['department_name']}, filter.department_name={department.name}")
                    continue
                filtered_summary.append(result)
            team_summary = filtered_summary
            print(f"team_progress_summary: applied team/department filters, team_summary={team_summary}")

    # Determine the template based on role
    if role == 'team-leader':
        template_name = 'home/summary.html'  # Team leaders use the summary page
    elif role == 'department-leader':
        template_name = 'reports/teamprogress_DL.html'
    else:  # senior-manager
        template_name = 'authentication/teamprogress_SM.html'
    print(f"team_progress_summary: template_name={template_name}")

    return team_summary, selected_date, form, template_name

# Dispatcher view to route to the appropriate dashboard based on role
@login_required
def dashboard_dispatcher(request):
    profile = Profile.objects.get(user=request.user)
    role = profile.role

    if role == 'senior-manager':
        return redirect('dashboard_SM')
    elif role == 'department-leader':
        return redirect('dashboard_DL')
    else:
        return redirect('dashboard')

# login_required ensures only authenticated users access views
@login_required
def home_vote_view(request):
    # if user has selected department and team
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
            # Renders voting page with user’s team/department info
            return render(request, 'home/voting.html', context)
    except UserSelection.DoesNotExist:
        #show department list instead
        pass

    departments = Department.objects.all()
    # renders voting page with department list
    return render(request, 'home/voting.html', {
        'departments': departments,
        'has_selection': False
    })

# Fetches teams
def get_teams(request):
    # department_id from GET request
    department_id = request.GET.get('department_id')
    teams = Team.objects.filter(department_id=department_id).values('id', 'team_name')
    # Returns JSON list of teams
    return JsonResponse(list(teams), safe=False)

# Main dashboard view for engineers and team leaders
@login_required
def dashboard(request):
    profile = Profile.objects.get(user=request.user)
    user_role = profile.role

    # Redirect Senior Managers and Department Leaders to their dashboards
    if user_role == 'senior-manager':
        return redirect('dashboard_SM')
    elif user_role == 'department-leader':
        return redirect('dashboard_DL')

    # Checks if user has a saved department/team selection
    try:
        user_selection = UserSelection.objects.get(user=request.user)
        has_selection = user_selection.department is not None and user_selection.team is not None
    except UserSelection.DoesNotExist:
        user_selection = None
        has_selection = False

    departments = Department.objects.all()

    # creates new voting session
    if request.method == 'POST' and has_selection:
        session, _ = Session.objects.get_or_create(
            team=user_selection.team,
            date=timezone.now(),
            defaults={'is_finished': False}
        )
        # Redirects to voting page with session ID
        return redirect('voting', session_id=session.id)

    # saves new department/team
    if request.method == 'POST' and not has_selection:
        dept_id = request.POST.get('department')
        team_id = request.POST.get('team')

        if dept_id and team_id:
            try:
                department = Department.objects.get(id=dept_id)
                team = Team.objects.get(id=team_id)

                # Create or update selection
                if not user_selection:
                    user_selection = UserSelection.objects.create(user=request.user, department=department, team=team)
                else:
                    user_selection.department = department
                    user_selection.team = team
                    user_selection.save()

                # Start new voting session
                session, _ = Session.objects.get_or_create(
                    team=team,
                    date=timezone.now(),
                    defaults={'is_finished': False}
                )

                # Success message for user
                messages.success(request, "Your department and team have been successfully selected.")
                return redirect('voting', session_id=session.id)

            except (Department.DoesNotExist, Team.DoesNotExist):
                # Invalid selection message
                messages.error(request, "Invalid department or team.")
        else:
            # Missing data message
            messages.error(request, "Please select both department and team.")

    # dashboard with selection state
    return render(request, 'home/home.html', {
        'departments': departments,
        'has_selection': has_selection,
        'department': user_selection.department if user_selection else None,
        'team': user_selection.team if user_selection else None,
        'user_role': user_role,
    })

# Handles voting
@login_required
def voting(request, session_id):
    profile = Profile.objects.get(user=request.user)
    # restricts voting to engineers and team leaders
    if profile.role not in ['engineer', 'team-leader']:
        messages.error(request, "You are not authorized to vote.")
        return redirect('dashboard_dispatcher')
    
    # active session by ID
    try:
        session = Session.objects.get(id=session_id, is_finished=False)
        team = session.team
    except Session.DoesNotExist:
        # Session invalid? back to dashboard
        messages.error(request, "Session not found or already finished.")
        return redirect('dashboard_dispatcher')
    
    # Loads all questions for voting cards
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
    
    # submitted votes
    if request.method == 'POST':
        print("POST data:", dict(request.POST))
        results = {}
        processed_cards = 0
        expected_cards = len(cards)
        card_ids = {card.id for card in cards}
        
        # Loops through each card’s vote
        for card_id in card_ids:
            try:
                card_id_str = str(card_id)
                # avoid duplicate POST issues
                trend = request.POST.getlist(f'responses[{card_id_str}][trend]')[0] if request.POST.getlist(f'responses[{card_id_str}][trend]') else None
                state = request.POST.getlist(f'responses[{card_id_str}][state]')[0] if request.POST.getlist(f'responses[{card_id_str}][state]') else None
                print(f"Processing card {card_id}: trend={trend}, state={state}")
                
                # invalid or missing votes
                if not trend or not state or trend not in ['0', '1', '2'] or state not in dict(Card.STATE_CHOICES):
                    print(f"Invalid or missing data for card {card_id}: trend={trend}, state={state}")
                    continue
                
                card = Card.objects.get(id=card_id, team=team)
                # Saves or updates user’s vote
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
                # Logs errors for debugging
                print(f"Error processing card {card_id}: {e}")
                continue
        
        # session results
        session.voting_results = {
            'votes': list(Vote.objects.filter(session=session).values(
                'user__username', 'card__question__text', 'trend', 'state'
            ))
        }
        # Marks session complete if all votes
        session.is_finished = processed_cards == expected_cards
        session.save()
        print(f"Session {session.id} finished: {session.is_finished}, results: {session.voting_results}, processed: {processed_cards}/{expected_cards}")
        # Success or warning
        if session.is_finished:
            messages.success(request, "Votes submitted successfully.")
        else:
            messages.warning(request, f"Only {processed_cards} of {expected_cards} votes processed. Please ensure all questions are answered.")
        return redirect('summary')
    
    # voting page with cards rendering
    return render(request, 'home/voting.html', {
        'team': team,
        'cards': cards,
        'trend_choices': Card.TREND_CHOICES,
    })

# vote summaries based on user role
@login_required
def summary(request):
    profile = Profile.objects.get(user=request.user)
    role = profile.role
    username = profile.user.username

    # Redirect Senior Managers and Department Leaders to their team progress pages
    if role == 'senior-manager':
        return redirect('teamprogress')
    elif role == 'department-leader':
        return redirect('teamprogress_DL')

    # default date to today
    today = timezone.now().date()

    # selected date from GET params
    selected_date = request.GET.get('date', str(today))
    try:
        selected_date = timezone.datetime.strptime(selected_date, "%Y-%m-%d").date()
    except ValueError:
        selected_date = today

    # user’s votes for selected date
    user_votes = Vote.objects.filter(
        user=request.user,
        created_at__date=selected_date
    ).select_related('card__question', 'session').order_by('-created_at')

    #  user’s department/team selection
    try:
        user_selection = UserSelection.objects.get(user=request.user)
        selected_department = user_selection.department
        selected_team = user_selection.team
    except UserSelection.DoesNotExist:
        selected_department = None
        selected_team = None

    # Use the reusable function for team leaders
    form = TeamProgressFilterForm(user=request.user, data=request.POST or None)
    team_summary, selected_date, form, template_name = team_progress_summary(
        user=request.user, role='team-leader', form=form, selected_date=selected_date
    )

    # user votes with timestamps
    formatted_votes = []
    for vote in user_votes:
        formatted_vote = {
            'question': vote.card.question.text,
            'trend': vote.trend,
            'state': vote.state,
            'time': vote.created_at.strftime("%H:%M")
        }
        formatted_votes.append(formatted_vote)

    # summary page with results
    return render(request, template_name, {
        'session_results': team_summary,  # Keep this for compatibility with summary.html
        'user_votes': formatted_votes,
        'user_role': role,
        'username': username,
        'selected_department': selected_department,
        'selected_team': selected_team,
        'selected_date': selected_date,
        'form': form,
    })