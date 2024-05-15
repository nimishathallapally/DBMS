from django.shortcuts import render
from django.http import HttpResponse
from .forms import NewEvent 


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
    return render(request,"app1/add_events.html",{'form':event}) 