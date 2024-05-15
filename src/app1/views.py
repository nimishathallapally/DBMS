from django.shortcuts import render
from django.http import HttpResponse
from .forms import NewEvent 
from django.template import loader
from .models import Event
from django.utils import timezone
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


def events(request):
    events = Event.objects.filter(event_start_date_time__date=timezone.now()).values()
    template = loader.get_template('app1/events.html')
    logging.warn(f'Events:{events}')
    context = {
        'events':events,
    }
    return HttpResponse(template.render(context, request))