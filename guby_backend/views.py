from django.shortcuts import render

# Create your views here.
from guby_backend.models import Roles


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
    return render(request, 'app/meetups.html', {})

def meetup_desc(request):
    return render(request, 'app/meetup_desc.html', {})

def meetup_add(request):
    return render(request, 'app/meetup_add.html', {})

def meetup_edit(request):
    return render(request, 'app/meetup_edit.html', {})

def event_index(request):
    return render(request, 'app/meetups/events.html', {})

def event_add(request):
    return render(request, 'app/event_add.html', {})
