from django.shortcuts import render
from django.http import HttpResponse
from .forms import NewEvent 
from django.template import loader
from .models import Event, Department
from django.utils import timezone
import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.models import Group 

def logout_view(request):
    logout(request)
    return redirect('Home-Page')  

@login_required
def add_event(request):  
    unauthorised_group = Group.objects.get(name='unauthorised')
    # Fetch usernames associated with the unauthorised group
    unauthorised_usernames = unauthorised_group.user_set.values_list('username', flat=True)
    if request.user.groups.filter(name='unauthorised').exists():
        return HttpResponse("You are not authorized to add events.")
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
        events = Event.objects.filter(event_start_date_time__date=timezone.now())
    
    else:
        events = Event.objects.filter(dept_id=selector, event_start_date_time__date=timezone.now())

    template = loader.get_template('app1/events.html')
    logging.warn(f'Events:{events}')
    unauthorised_usernames = Group.objects.get(name='unauthorised').user_set.values_list('username', flat=True)
    
    context = {
        'events':events,
        'depts':Department.objects.all(),
        'unauthorised_usernames': unauthorised_usernames
    }
    return HttpResponse(template.render(context, request))