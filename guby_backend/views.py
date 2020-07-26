from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

import guby_backend.models as models
from guby_backend.utils import has_ownership, get_own_meetup_ids
import guby_backend.chat as chat
from .forms import *

import logging
import traceback
import sys
import random

logger = logging.getLogger(__name__)

User = get_user_model()


class SignUpView(CreateView):
    form_class = GubyUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'app/user_register.html'

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

@login_required()
def meetup_index(request):
    meetup_ids = get_own_meetup_ids(request.user)
    # get all meetups where user is owner, not just creator
    meetups = Meetup.objects.filter(pk__in=meetup_ids)

    return render(request, 'app/meetups.html', {'meetups': meetups})

@login_required()
def meetup_add(request):
     form = MeetupForm(request.POST or None)  
     if form.is_valid():  
        meetup = form.save(commit=False)  
        meetup.creator = request.user
        meetup.save()
        # create group to handle meetup ownership
        owner_group, created = Group.objects.get_or_create(name=f'meetup-owner#{meetup.id}')
        owner_group.user_set.add(request.user)
        #TODO handle errors
        return redirect('/app/meetups')  

     return render(request, 'app/meetup_add.html', {'form': form})

@login_required()
@has_ownership
def meetup_edit(request, meetup_id):
    meetup = get_object_or_404(Meetup, pk=meetup_id)

    form = MeetupForm(request.POST or None, instance = meetup)
    if form.is_valid():
        form.save()
        #TODO handle errors
        return redirect('/app/meetups/')

    return render(request, 'app/meetup_edit.html', {"form": form, "meetup_id": meetup.id})

@login_required()
@has_ownership
def meetup_delete(request, meetup_id):
    meetup = get_object_or_404(Meetup, pk=meetup_id)
    form = MeetupDeleteForm(instance=meetup)

    if request.method == 'POST':
        meetup.delete()
        return redirect('/app/meetups/')

    return render(request, 'app/meetup_delete.html', {"form": form, "meetup_id": meetup.id})

@login_required()
@has_ownership
def meetup_owner_index(request, meetup_id):
   
    if request.method == 'GET':
        meetup = get_object_or_404(Meetup, pk=meetup_id)

        users = User.objects.filter(groups__name=f'meetup-owner#{meetup_id}')
        enable_remove = (len(users) > 1) # no group should become orphan by deleting all owners

        return render(request, 'app/meetup_owner_index.html', {'meetup': meetup, 'owners': users, 'enable_remove': enable_remove})
    
@login_required()
@has_ownership
def meetup_owner_add(request, meetup_id):
   
    if request.method == 'GET':
        return render(request, 'app/meetup_add_owner.html', {'meetup_id': meetup_id})
         # create group to handle meetup ownership
    
    if request.method == 'POST':
        userid = request.POST['meetup-userid']
        new_user = User.objects.get(username=userid)
        owner_group, created = Group.objects.get_or_create(name=f'meetup-owner#{meetup_id}')
        owner_group.user_set.add(new_user)
    #     #TODO handle errors
        return redirect(f'/app/meetups/{meetup_id}/owner/')  

@login_required()
@has_ownership
def meetup_owner_delete(request, meetup_id, user_id):
   
    if request.method == 'GET':
        owner = User.objects.get(id=user_id)
        owner_group, created = Group.objects.get_or_create(name=f'meetup-owner#{meetup_id}')
        owner_group.user_set.remove(owner)
    #     #TODO handle errors
        return redirect(f'/app/meetups/{meetup_id}/owner/')  

@login_required()
@has_ownership
def event_index(request, meetup_id):
    # check if login user is owner of meetupid
    meetup = Meetup.objects.get(id=meetup_id)
    events = Event.objects.filter(meetup=meetup_id)
    return render(request, 'app/events.html', {'meetup': meetup, 'events': events})

@login_required()
@has_ownership
def event_add(request, meetup_id):
    form = EventForm(request.POST or None)
    if form.is_valid():
        try:
            meetup = Meetup.objects.get(id=meetup_id)
            model = form.save(commit=False)
            channel_name = str(model.name) + '_' + str(random.randint(0, 10000))
            model.channel = channel_name
            channel_created = chat.create_channel(channel_name)
            logger.info("Rocket channel created {}".format(channel_created))
            model.meetup = meetup
            model.status = Event.STATUS_CREATED
            model.save()
            return redirect(f'/app/meetups/{meetup_id}/events/')
        except Exception as e:
            logger.exception(e, exc_info=True)
    return render(request, 'app/event_add.html', {'form': form, 'meetup_id': meetup_id})

@login_required()
@has_ownership
def event_edit(request, meetup_id, event_id):
    event = get_object_or_404(Event, pk=event_id)
    form = EventForm(request.POST or None, instance=event)

    if form.is_valid():
        form.save()
        return redirect(f'/app/meetups/{meetup_id}/events/')

    return render(request, 'app/event_edit.html', {"form": form, "meetup_id": meetup_id, "event": event})

@login_required()
@has_ownership
def event_delete(request, meetup_id, event_id):
    event = get_object_or_404(Event, pk=event_id)
    form = EventDeleteForm(instance=event)

    if request.method == 'POST':
        event.delete()
        return redirect(f'/app/meetups/{meetup_id}/events/')

    return render(request, 'app/event_delete.html', {"form": form, "meetup_id": meetup_id, "event": event})
