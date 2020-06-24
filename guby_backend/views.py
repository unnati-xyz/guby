from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
import logging
import traceback

logger = logging.getLogger(__name__)

import guby_backend.models as models
from .forms import *

def get_roles(request):
    role_objects = Roles.objects.get()
    context = {
        "roles" : role_objects 
    }

def get_rolename(request, id):
    role_name = Roles.objects.get(pk=id)
    context = {
        "role_name" : role_name
    }

def speaker_index(request):
    return render(request, 'app/speakers.html', {})

def speaker_add(request):
    return render(request, 'app/speaker_add.html', {})

def meetup_index(request):
    meetups = Meetup.objects.all()
    return render(request, 'app/meetups.html', {'meetups': meetups})

def meetup_desc(request):
    return render(request, 'app/meetup_desc.html', {})

def meetup_add(request):
     form = MeetupForm(request.POST or None)  
   
     if form.is_valid():  
         meetup = form.save()  
         #TODO handle errors
         return redirect('/app/meetups')  

     return render(request, 'app/meetup_add.html', {'form': form})

def meetup_edit(request, meetup_id):
    meetup = get_object_or_404(Meetup, pk=meetup_id)

    form = MeetupForm(request.POST or None, instance = meetup)
    if form.is_valid():
        form.save()
        #TODO handle errors
        return redirect('/app/meetups/')

    return render(request, 'app/meetup_edit.html', {"form": form, "meetup_id": meetup.id})

def meetup_delete(request, meetup_id):
    meetup = get_object_or_404(Meetup, pk=meetup_id)
    form = MeetupDeleteForm(instance=meetup)

    if request.method == 'POST':
        meetup.delete()
        return redirect('/app/meetups/')

    return render(request, 'app/meetup_delete.html', {"form": form, "meetup_id": meetup.id})

def event_index(request, meetup_id):
    events = Event.objects.filter(meetup=meetup_id)
    return render(request, 'app/events.html', {'events': events})

def event_add(request, meetup_id):
    form = EventForm(request.POST or None)

    if form.is_valid():
        model = form.save()
        #TODO handle errors
        return redirect('/app/meetups/')

    return render(request, 'app/event_add.html', {'form': form})


def event_edit(request, meetup_id, event_id):
    event = get_object_or_404(Event, pk=event_id)
    form = EventForm(request.POST or None, instance = event)

    if form.is_valid():
        form.save()
        return redirect(f'/app/meetups/{meetup_id}/events/')

    return render(request, 'app/event_edit.html', {"form": form, "event": event})

def event_delete(request, meetup_id, event_id):
    event = get_object_or_404(Event, pk=event_id)
    form = EventDeleteForm(instance=event)

    if request.method == 'POST':
        event.delete()
        return redirect(f'/app/meetups/{meetup_id}/events/')

    return render(request, 'app/event_delete.html', {"form": form, "event": event})
