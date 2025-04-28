from django import forms

class OverviewFilterForm (form.Form):

    DEPARTMENT_CHOICES = [
     ('department1', 'Department 1')
     ('department2', 'Department 2')
     ('department3', 'Department 3')

    ]

    DURATION_CHOICES = [
        ('1m', '1 Month')
        ('6m', '6 Month')
        ('1y', '1 Year')
    ]
    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES)
    duration = forms.ChoiceField(choices=DURATION_CHOICES)