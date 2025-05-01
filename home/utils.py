from django.utils import timezone
from django.db.models import Count
from home.models import Vote, UserSelection
import datetime  # Import datetime to use datetime.date

# Saves or updates a vote for a user in a session
def save_unique_vote(user, card, session, trend, state):
    vote, created = Vote.objects.update_or_create(
        user=user,
        card=card,
        session=session,
        defaults={'trend': trend, 'state': state}
    )
    return vote

#    maps a trend value to a color
def get_trend_color(trend):

    # The trend value 0 - 2 : red yellow green
    return {0: "Red", 1: "Yellow", 2: "Green"}.get(trend, "Yellow")

def get_team_summary(user, role, selected_date):
    #  Returns team voting summary
    print(f"get_team_summary: user={user.username}, role={role}, selected_date={selected_date}")
    # Ensure selected_date is a datetime.date object
    if isinstance(selected_date, str):
        selected_date = timezone.datetime.strptime(selected_date, "%Y-%m-%d").date()
        print(f"get_team_summary: parsed selected_date to {selected_date}")
    elif not isinstance(selected_date, datetime.date):
        raise ValueError("selected_date must be a datetime.date object or a string in 'YYYY-MM-DD' format")

    # Fetch user's team and department based on role
    user_team = None
    user_department = None
    try:
        user_selection = UserSelection.objects.get(user=user)
        user_team = user_selection.team
        user_department = user_selection.department
        print(f"get_team_summary: user_selection found, team={user_team}, department={user_department}")
    except UserSelection.DoesNotExist:
        print("get_team_summary: No UserSelection found for user")

    # Filter votes based on role
    if role == 'team-leader':
        if not user_team:
            print("get_team_summary: No team for team-leader, returning empty list")
            return []
        # Team leaders see only their team's votes
        votes = Vote.objects.filter(
            card__team=user_team,
            created_at__date=selected_date
        )
        print(f"get_team_summary: team-leader votes count={votes.count()}")
    elif role == 'department-leader':
        if not user_department:
            print("get_team_summary: No department for department-leader, returning empty list")
            return []
        # Department leaders see votes for all teams in their department
        votes = Vote.objects.filter(
            card__team__department=user_department,
            created_at__date=selected_date
        )
        print(f"get_team_summary: department-leader votes count={votes.count()}")
    elif role == 'senior-manager':
        # Senior managers see all votes
        votes = Vote.objects.filter(
            created_at__date=selected_date
        )
        print(f"get_team_summary: senior-manager votes count={votes.count()}")
        if votes.exists():
            for vote in votes:
                print(f"get_team_summary: vote={vote}, user={vote.user.username}, team={vote.card.team}, department={vote.card.team.department}, created_at={vote.created_at}")
        else:
            # Debug why votes are not found
            all_votes = Vote.objects.all()
            print(f"get_team_summary: Total votes in database={all_votes.count()}")
            for vote in all_votes:
                print(f"get_team_summary: Existing vote={vote}, user={vote.user.username}, created_at={vote.created_at}, date_part={vote.created_at.date()}")
    else:
        print("get_team_summary: Invalid role, returning empty list")
        return []

    # Aggregate votes by team, question, trend, and state
    vote_summary = votes.values(
        'card__team__team_name',
        'card__team__department__name',
        'card__question__text',
        'trend',
        'state'
    ).annotate(
        vote_count=Count('id')
    )
    print(f"get_team_summary: vote_summary={vote_summary}")

    # Process the summary into a more usable format
    summary = []
    team_entries = {}

    # counts for each team question and its values
    for entry in vote_summary:
        team_name = entry['card__team__team_name']
        department_name = entry['card__team__department__name']
        question = entry['card__question__text']
        trend = entry['trend']
        state = entry['state']
        count = entry['vote_count']

        print(f"get_team_summary: Processing vote entry - team={team_name}, dept={department_name}, question={question}, trend={trend}, state={state}, count={count}")

        # unique key for the question
        key = (team_name, question)

        if key not in team_entries:
            team_entries[key] = {
                'team_name': team_name,
                'department_name': department_name,
                'question': question,
                'red_count': 0,
                'yellow_count': 0,
                'green_count': 0,
                'state_counts': {},
            }

        # update trend counts
        if trend == 0:
            team_entries[key]['red_count'] += count
        elif trend == 1:
            team_entries[key]['yellow_count'] += count
        elif trend == 2:
            team_entries[key]['green_count'] += count

        # update state counts
        team_entries[key]['state_counts'][state] = team_entries[key]['state_counts'].get(state, 0) + count

    # Determine most common trend and state for each question
    for key, data in team_entries.items():
        # most common trend
        trend_counts = {
            0: data['red_count'],
            1: data['yellow_count'],
            2: data['green_count']
        }
        most_common_trend = max(trend_counts.items(), key=lambda x: x[1])[0] if any(trend_counts.values()) else 1  # Default to yellow if no votes
        trend_color = get_trend_color(most_common_trend)

        # most common state
        state_counts = data['state_counts']
        most_common_state = max(state_counts.items(), key=lambda x: x[1])[0] if state_counts else 'stable'

        # final entry
        entry = {
            'team_name': data['team_name'],
            'department_name': data['department_name'],
            'question': data['question'],
            'red_count': data['red_count'],
            'yellow_count': data['yellow_count'],
            'green_count': data['green_count'],
            'trend': most_common_trend,
            'trend_color': trend_color,
            'state': most_common_state,
        }
        summary.append(entry)

    return summary