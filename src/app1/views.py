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
from dateutil.parser import parse



def add_event(request):  
    if request.method == "POST":
        #print("Postingggggg")
        #import pdb; pdb.set_trace()
        ne=request.POST.dict()

        ne['event_start_date_time']=parse(ne['event_start_date_time'])
        ne['event_end_date_time']=parse(ne['event_end_date_time'])
        event = NewEvent(ne)
        #print(event)
        if event.is_valid():
            #print("vaaliddddd")
            event.save()
            return HttpResponse("Success")
        else:
            print("not valid")  
    event=NewEvent()
    return render(request,"app1/backup.html",{'form':event}) 


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
    context = {
        'events':events_qs,
        'depts':Department.objects.all(),
        'agenda':get_agenda(),
        'is_today':is_today,
        'show_date': req_datetime
    }
    return HttpResponse(template.render(context, request))

def get_agenda():
    agenda={}
    for i in range(1,8):
        curr_date = timezone.now()+relativedelta(days=i)
        agenda[curr_date] = Event.objects.filter(event_start_date_time__date=curr_date).order_by('event_start_date_time')
    logging.warn(f'Agenda:{agenda}')
    return agenda


