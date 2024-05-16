from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import NewEvent 
from .models import Event, Venue ,Club, Department
import json
from django.template import loader
from .models import Event, Department, Favorites
from django.utils import timezone
from dateutil.relativedelta import relativedelta
import logging
from dateutil.parser import parse

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.models import Group 
import datetime

def logout_view(request):
    logout(request)
    return redirect('Home-Page')  

@login_required
def add_event(request):
    #import pdb;pdb.set_trace()  
    # Fetch usernames associated with the authorised group
    if not request.user.groups.filter(name='authorised').exists():
        return HttpResponse("You are not authorized to add events.")
    if request.method == "POST":
        print("Postingggggg")
        #import pdb; pdb.set_trace()
        ne=request.POST.dict()

        ne['event_start_date_time']=parse(ne['event_start_date_time'])
        ne['event_end_date_time']=parse(ne['event_end_date_time'])
        ne['event_creation_date_time']=datetime.datetime.now()
        ne['user']=request.user
        ne['dept']=Department.objects.filter(head_email=request.user) | Department.objects.filter(club__head_email=request.user)
        ne['dept']=ne['dept'].values()[0]["id"]
        event = NewEvent(ne)
        #print(event)
        if event.is_valid():
            #print("vaaliddddd")
            event.save()
            return HttpResponseRedirect('/events/')
        else:
            print("not valid")  
    event=NewEvent()
    return render(request,"app1/backup.html",{'form':event}) 


def fav_event(request, eventid):
    if request.user.is_authenticated:
        event = Event.objects.filter(id=eventid).first()
        fav, created = Favorites.objects.get_or_create(user=request.user, event=event)
        logging.warn(f'Fav done for {fav.event} by {fav.user}')
        return JsonResponse({"status":"success"})
    else:
        return JsonResponse({"status":"error"})

def unfav_event(request, eventid):
    if request.user.is_authenticated:
        event = Event.objects.filter(id=eventid).first()
        Favorites.objects.filter(user=request.user, event=event).delete()
        # logging.warn(f'Fav removed for {fav.event} by {fav.user}')
        return JsonResponse({"status":"success"})
    else:
        return JsonResponse({"status":"error"})


def delete_event(request, eventid):
    rm_event = Event.objects.filter(user=request.user, id=eventid).delete()
    return HttpResponseRedirect('/events/')


def list_venue(request):
    venue = []
    if request.GET.get("start_time") and request.GET.get("end_time"):
        #import pdb; pdb.set_trace()
        st = request.GET.get("start_time") 
        st=parse(st)
        et = request.GET.get("end_time")
        et=parse(et)
        #print(st, et)
        available = Venue.objects.exclude(event__event_start_date_time__lte=et,event__event_end_date_time__gte=st)
        #print(available)
        for item in available:
            venue.append({"name": str(item.pk) , "value":str(f"{item.building_name}:{item.location}")})
    return JsonResponse(venue, safe=False) 

def list_club(request):
    club=[]
    user=request.user
    available=Club.objects.filter(head_email=user) | Club.objects.filter(dept__head_email=user)  
    for item in available:
        club.append({"name":str(item.pk),"value":str(f"{item.name}")})
    return JsonResponse(club,safe=False)


def events(request, datestr=None, selector='all'):

    is_today = True
    req_datetime = None
    my_fav_event_ids = None

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

    elif selector == 'fav':
        my_fav_event_ids = list(Favorites.objects.filter(user=request.user, event__in=events_qs.all()).values_list("event_id", flat=True))
        events_qs = Event.objects.filter(id__in=my_fav_event_ids)

    else:
        logging.warn(f'Selecting dept_id:{selector}')
        events_qs = events_qs.filter(dept_id=selector)

    if request.user.is_authenticated:
        if my_fav_event_ids is None:
            my_fav_event_ids = list(Favorites.objects.filter(user=request.user, event__in=events_qs.all()).values_list("event_id", flat=True))
            logging.warn(f'My fave events:{my_fav_event_ids}')

    events_qs = events_qs.order_by('event_start_date_time')

    template = loader.get_template('app1/events.html')
    # logging.warn(f'Events:{events_qs}')
    can_add_event = request.user.groups.filter(name='authorised').exists()

    # Group.objects.get(name='unauthorised').user_set.values_list('username', flat=True)
    
    context = {
        'events':events_qs,
        'depts':Department.objects.all(),
        'agenda':get_agenda(),
        'is_today':is_today,
        'show_date': req_datetime,
        'can_add_event': can_add_event,
        'my_fav_event_ids' : my_fav_event_ids,
        'selector': selector,
    }
    return HttpResponse(template.render(context, request))

def get_agenda():
    agenda={}
    for i in range(1,8):
        curr_date = timezone.now()+relativedelta(days=i)
        agenda[curr_date] = Event.objects.filter(event_start_date_time__date=curr_date).order_by('event_start_date_time')
    # logging.warn(f'Agenda:{agenda}')
    return agenda


