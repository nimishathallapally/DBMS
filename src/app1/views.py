from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .forms import NewEvent 
from .models import Event, Venue
import json
from django.template import loader
from .models import Event, Department
from django.utils import timezone
from dateutil.relativedelta import relativedelta
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
    # Fetch usernames associated with the authorised group
    if not request.user.groups.filter(name='authorised').exists():
        return HttpResponse("You are not authorized to add events.")
    if request.method == "POST":
        #import pdb; pdb.set_trace()
        event = NewEvent(request.POST)
        if event.is_valid():
            event.save()
            return HttpResponse("Success")  
    event=NewEvent()
    return render(request,"app1/backup.html",{'form':event}) 

def list_venue(request):
    venue = [{"name": "default_venue", "value": "myvenue"}]
    if request.GET.get("start_time") and request.GET.get("end_time"):
        
        st = request.GET.get("start_time") 
        et = request.GET.get("end_time")
        available = Venue.objects.exclude(event__event_start_date_time__lte=et,event__event_end_date_time__gte=st)
        for item in available:
            venue.append({"name": str(item), "value": str(item)})
    # return JsonResponse(json.dumps(venue), safe=False)
    return JsonResponse(venue, safe=False)    


def events(request, datestr=None, selector='all'):

    is_today = True
    req_datetime = None

    if not datestr:
        req_datetime = timezone.now()
    else:
        is_today = False
        req_datetime = timezone.datetime.strptime(datestr, '%Y%m%d')
        if req_datetime.strftime('%Y%m%d') == timezone.datetime.now().strftime('%Y%m%d'):
            is_today = True
    
    logging.warn(f'Requesting events for Date:{req_datetime}')

    events_qs = Event.objects.filter(event_start_date_time__date=req_datetime)


    if selector == 'all':
        pass
        # events = Event.objects.filter(event_start_date_time__date=req_datetime).order_by('event_start_date_time')

    else:
        logging.warn(f'Selecting dept_id:{selector}')
        events_qs = events_qs.filter(dept_id=selector)

    events_qs = events_qs.order_by('event_start_date_time')

    template = loader.get_template('app1/events.html')
    logging.warn(f'Events:{events_qs}')
    can_add_event = request.user.groups.filter(name='authorised').exists()

    # Group.objects.get(name='unauthorised').user_set.values_list('username', flat=True)
    
    context = {
        'events':events_qs,
        'depts':Department.objects.all(),
        'agenda':get_agenda(),
        'is_today':is_today,
        'show_date': req_datetime,
        'can_add_event': can_add_event
    }
    return HttpResponse(template.render(context, request))

def get_agenda():
    agenda={}
    for i in range(1,8):
        curr_date = timezone.now()+relativedelta(days=i)
        agenda[curr_date] = Event.objects.filter(event_start_date_time__date=curr_date).order_by('event_start_date_time')
    logging.warn(f'Agenda:{agenda}')
    return agenda


