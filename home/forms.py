from django import forms
from django.utils import timezone  # Correct import for timezone
from home.models import Department, Team, UserSelection

class TeamProgressFilterForm(forms.Form):
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=False,
        empty_label="All Departments"
    )
    team = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        required=False,
        empty_label="All Teams"
    )
    duration = forms.ChoiceField(
        choices=[
            ('', 'All Time'),
            ('7', 'Last 7 Days'),
            ('30', 'Last 30 Days'),
            ('90', 'Last 90 Days'),
        ],
        required=False
    )
    date = forms.DateField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'flatpickr'}),
        initial=timezone.now().date  # Now this will work
    )

    def __init__(self, *args, **kwargs):
        # Extract user from kwargs, if provided
        user = kwargs.pop('user', None)
        print(f"TeamProgressFilterForm: Initializing with user={user}")
        super(TeamProgressFilterForm, self).__init__(*args, **kwargs)
        self.user = user

        if user and hasattr(user, 'profile'):
            role = user.profile.role
            print(f"TeamProgressFilterForm: User role={role}")
            selected_department = None
            try:
                user_selection = UserSelection.objects.get(user=user)
                selected_department = user_selection.department
                print(f"TeamProgressFilterForm: user_selection found, selected_department={selected_department}")
            except UserSelection.DoesNotExist:
                print("TeamProgressFilterForm: No UserSelection found for user")

            # Adjust fields based on role
            if role == 'team-leader':
                # Team leaders don't need team, department, or date selection
                self.fields.pop('team', None)
                self.fields.pop('department', None)
                self.fields.pop('date', None)
                print("TeamProgressFilterForm: Removed team, department, and date fields for team-leader")
            elif role == 'department-leader':
                # Department leaders can select teams within their department
                self.fields.pop('department', None)  # They can't change department
                if selected_department:
                    self.fields['team'].queryset = Team.objects.filter(department=selected_department)
                    print(f"TeamProgressFilterForm: Set team queryset to {self.fields['team'].queryset} for department-leader")
                else:
                    self.fields['team'].queryset = Team.objects.none()
                    print("TeamProgressFilterForm: No selected department, team queryset set to none for department-leader")
            else:  # senior-manager
                # Senior managers can select both department and team
                # Dynamically update teams based on selected department
                print("TeamProgressFilterForm: Processing for senior-manager")
                if self.data and 'department' in self.data:
                    try:
                        dept_id = int(self.data.get('department'))
                        self.fields['team'].queryset = Team.objects.filter(department_id=dept_id)
                        print(f"TeamProgressFilterForm: Updated team queryset to {self.fields['team'].queryset} based on department_id={dept_id}")
                    except (ValueError, TypeError):
                        self.fields['team'].queryset = Team.objects.none()
                        print("TeamProgressFilterForm: Invalid department ID, team queryset set to none")