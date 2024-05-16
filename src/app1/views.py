from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .forms import NewEvent 
from .models import Event, Venue
import json


def hi(request):
    return render(request, 'app1/index.html', {})

def event(request):  
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
    return JsonResponse(json.dumps(venue), safe=False)