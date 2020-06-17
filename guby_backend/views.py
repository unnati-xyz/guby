from django.shortcuts import render
from django.contrib import messages
import logging
import traceback

logger = logging.getLogger(__name__)

# Create your views here.
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
    return render(request, 'app/meetups.html', {})

def meetup_desc(request):
    return render(request, 'app/meetup_desc.html', {})

def meetup_add(request):
    if request.method == 'GET':
        form = MeetupAddForm()
    if request.method == 'POST':
        form = MeetupAddForm(request.POST)
        try:
            if form.is_valid():
                meetup_model = models.Meetup(name=form.cleaned_data['name'],
                                            description=form.cleaned_data['description'],
                                            co_organizer_emails=form.cleaned_data['coorganize_email_id'])
                meetup_model.save()
                messages.success(request, 'Meetup successfully created')
        except Exception as e:
            logger.exception(e, exc_info=True)
            messages.error(request, 'Meeting could not be created, {}'.format(e))

    
    return render(request, 'app/meetup_add.html', {'form':form})

def meetup_edit(request):
    if request.method == 'GET':
        form = MeetupAddForm(initial={"name": "RubyGals", "description": "gals gals this is ruby!", "coorganize_email_id": "sha@ta.com,"})
        return render(request, 'app/meetup_edit.html', {"form": form})

    elif request.method == 'POST':
        form = MeetupAddForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            return messages.success(request, 'Meetup successfully updated')


def meetup_delete(request):
    if request.method == 'GET':
        form = MeetupDeleteForm(initial={"name": "RubyGals", "description": "gals gals this is ruby!", "coorganize_email_id": "sha@ta.com,"})
        return render(request, 'app/meetup_delete.html', {"form": form})

    elif request.method == 'POST':
        form = MeetupDeleteForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            return messages.success(request, 'Meetup successfully deleted')

def event_index(request):
    return render(request, 'app/meetups/events.html', {})

def event_add(request):
    if request.method == 'GET':
        form = EventAddForm()
        return render(request, 'app/event_add.html', {'form': form})

    elif request.method == 'POST':
        form = EventAddForm(request.POST)
        try:
            if form.is_valid():
                print(form.cleaned_data)
                # meetup_model = models.Event(
                #                     start_date = form.cleaned_data['start_date']
                # )
                # meetup_model.save()
                return messages.success(request, 'Meetup successfully created')
        except Exception as e:
            logger.exception(e, exc_info=True)
            messages.error(request, 'Meeting could not be created, {}'.format(e))

def event_edit(request):
    if request.method == 'GET':
        form = EventAddForm(initial={'start_date': '2020-06-20 10:30', 'end_date': '2020-06-21 10:30', 'video_lounges': 'General,', 'chat_rooms': 'General,'})
        return render(request, 'app/event_add.html', {'form': form})

    if request.method == 'POST':
        form = EventAddForm(request.POST)
        try:
            if form.is_valid():
                print(form.cleaned_data)
                # meetup_model = models.Event(
                #                     start_date = form.cleaned_data['start_date']
                # )
                # meetup_model.save()
                return messages.success(request, 'Meetup successfully created')
        except Exception as e:
            logger.exception(e, exc_info=True)
            messages.error(request, 'Meeting could not be created, {}'.format(e))

def event_delete(request):
    if request.method == 'GET':
        form = EventDeleteForm(initial={'start_date': '2020-06-20 10:30', 'end_date': '2020-06-21 10:30', 'video_lounges': 'General,', 'chat_rooms': 'General,'})
        return render(request, 'app/event_add.html', {'form': form})

    if request.method == 'POST':
        form = EventAddForm(request.POST)
        try:
            if form.is_valid():
                print(form.cleaned_data)
                # meetup_model = models.Event(
                #                     start_date = form.cleaned_data['start_date']
                # )
                # meetup_model.save()
                return messages.success(request, 'Meetup successfully created')
        except Exception as e:
            logger.exception(e, exc_info=True)
            messages.error(request, 'Meeting could not be created, {}'.format(e))