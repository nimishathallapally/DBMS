from django import forms
from django.core.exceptions import ValidationError
import datetime

from .models import Event

class NewEvent(forms.ModelForm):
    def valid(self):
       data1 = self.cleaned_data['event_start_date_time']

       # Check if a date is not in the past.
       if data1 < datetime.date.today():
           raise ValidationError('Invalid date - A past event cannot be registered')

       # Remember to always return the cleaned data.
       return data1


    class Meta:
        model = Event
        fields = ['name','description','event_start_date_time','event_end_date_time']
        labels = {'name': ('Event Name'),'description': ("Event Desciption"),\
                  'event_start_date_time': ("Event start time"),\
                    'event_end_date_time': ("Event end time")}
        