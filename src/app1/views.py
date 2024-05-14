from django.shortcuts import render
from django.http import HttpResponse
from .forms import NewEvent 


def hi(request):
    return render(request, 'app1/index.html', {})

def event(request):  
    event = NewEvent()  
    return render(request,"app1/add_events.html",{'form':event}) 