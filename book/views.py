from django.shortcuts import render
from .models import Event, EventImage
#from django.http import HttpResponse
#from 
# Create your views here.




def home(request):
    try:
        events = Event.objects.all()
        event_data = [(event, EventImage.objects.filter(event=event)) for event in events]
        context = {"event_data": event_data}
        return render(request, 'yb-base.html', context)
    except Event.DoesNotExist:
        return render(request, "404.html")
