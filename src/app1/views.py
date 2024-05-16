from django.shortcuts import render
from django.http import HttpResponse
from .forms import NewEvent 
from django.template import loader
from .models import Event, Department
from django.utils import timezone
from dateutil.relativedelta import relativedelta
import logging


def add_event(request):  
    if request.method == "POST":
        #import pdb; pdb.set_trace()
        event = NewEvent(request.POST)
        if event.is_valid():
            event.save()
            return HttpResponse("Success")  
    event=NewEvent()
    return render(request,"app1/add_events.html",{'form':event}) 


def events(request, selector='all'):

    if selector == 'all':
        events = Event.objects.filter(event_start_date_time__date=timezone.now()).order_by('event_start_date_time')
    
    else:
        events = Event.objects.filter(dept_id=selector, event_start_date_time__date=timezone.now()).order_by('event_start_date_time')

    template = loader.get_template('app1/events.html')
    logging.warn(f'Events:{events}')
    context = {
        'events':events,
        'depts':Department.objects.all(),
        'agenda':get_agenda()
    }
    return HttpResponse(template.render(context, request))

def get_agenda():
    agenda={}
    for i in range(1,8):
        curr_date = timezone.now()+relativedelta(days=i)
        agenda[curr_date] = Event.objects.filter(event_start_date_time__date=curr_date).order_by('event_start_date_time')
    logging.warn(f'Agenda:{agenda}')
    return agenda


