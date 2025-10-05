from django import forms
from .models import Habit, HabitLog

class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['title', 'description', 'goal_days']

class LogForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = HabitLog
        fields = ['date', 'completed', 'notes']