from django import forms
from .models import CountdownTimer

class CountdownTimerForm(forms.ModelForm):
    class Meta:
        model = CountdownTimer
        fields = ('seconds',)