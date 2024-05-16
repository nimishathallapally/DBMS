from django import forms
from django.core.exceptions import ValidationError
import datetime

from .models import Event

class NewEvent(forms.ModelForm):



    class Meta:
        model = Event
        fields = ['name','description','venue','event_start_date_time','event_end_date_time','event_creation_date_time','user','club','dept']
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'name of event'}),
            'description':forms.Textarea(attrs={'class':'form-control'}),
            'venue':forms.Select(attrs={'class':'form-control'}),
            'club':forms.Select(attrs={'class':'form-control'}),
            'event_start_date_time':forms.DateTimeInput(attrs={'class':'form-control'},),
            'event_end_date_time':forms.DateTimeInput(attrs={'class':'form-control'}),
        }
        
