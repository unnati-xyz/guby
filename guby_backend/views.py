from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

import guby_backend.models as models
from guby_backend.utils import has_ownership, get_own_meetup_ids, create_inactive_user
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
        "roles": role_objects
    }


def get_rolename(request, id):
    role_name = Roles.objects.get(pk=id)
    context = {
        "role_name": role_name
    }


@login_required()
def meetup_index(request):
    logger.info(f"request meetup index for user {request.user}")
    meetup_ids = get_own_meetup_ids(request.user)
    # get all meetups where user is owner, not just creator
    meetups = Meetup.objects.filter(pk__in=meetup_ids)

    return render(request, 'app/meetups.html', {'meetups': meetups})


@login_required()
def meetup_add(request):
    logger.info(f"{request.method} request meetup add by user {request.user}")
    form = MeetupForm(request.POST or None)
    if form.is_valid():
        meetup = form.save(commit=False)
        meetup.creator = request.user
        meetup.save()
        # create group to handle meetup ownership
        owner_group, created = Group.objects.get_or_create(
            name=f'meetup-owner#{meetup.id}')
        owner_group.user_set.add(request.user)
        # TODO handle errors
        return redirect('/app/meetups')

    return render(request, 'app/meetup_add.html', {'form': form})


@login_required()
@has_ownership
def meetup_edit(request, meetup_id):
    logger.info(
        f"{request.method} request meetup edit by user {request.user} meetup id {meetup_id}")
    meetup = get_object_or_404(Meetup, pk=meetup_id)

    form = MeetupForm(request.POST or None, instance=meetup)
    if form.is_valid():
        form.save()
        # TODO handle errors
        return redirect('/app/meetups/')

    return render(request, 'app/meetup_edit.html', {"form": form, "meetup_id": meetup.id})


@login_required()
@has_ownership
def meetup_delete(request, meetup_id):
    logger.info(
        f"{request.method} request meetup delete by user {request.user} meetup id {meetup_id}")
    meetup = get_object_or_404(Meetup, pk=meetup_id)
    form = MeetupDeleteForm(instance=meetup)

    if request.method == 'POST':
        meetup.delete()
        return redirect('/app/meetups/')

    return render(request, 'app/meetup_delete.html', {"form": form, "meetup_id": meetup.id})


@login_required()
@has_ownership
def meetup_owner_index(request, meetup_id):
    logger.info(
        f"{request.method} request meetup owner index by user {request.user} meetup id {meetup_id}")

    if request.method == 'GET':
        meetup = get_object_or_404(Meetup, pk=meetup_id)

        users = User.objects.filter(groups__name=f'meetup-owner#{meetup_id}')
        # no group should become orphan by deleting all owners
        enable_remove = (len(users) > 1)

        return render(request, 'app/meetup_owner_index.html', {'meetup': meetup, 'owners': users, 'enable_remove': enable_remove})


@login_required()
@has_ownership
def meetup_owner_add(request, meetup_id):
    logger.info(
        f"{request.method} request meetup owner add by user {request.user} meetup id {meetup_id}")

    if request.method == 'GET':
        return render(request, 'app/meetup_add_owner.html', {'meetup_id': meetup_id})
        # create group to handle meetup ownership

    if request.method == 'POST':
        userid = request.POST['meetup-userid']
        new_user = User.objects.get(email=userid)
        owner_group, created = Group.objects.get_or_create(
            name=f'meetup-owner#{meetup_id}')
        owner_group.user_set.add(new_user)
    #     #TODO handle errors
        return redirect(f'/app/meetups/{meetup_id}/owner/')


@login_required()
@has_ownership
def meetup_owner_delete(request, meetup_id, user_id):
    logger.info(
        f"{request.method} request meetup owner delete by user {request.user} meetup id {meetup_id}")

    if request.method == 'GET':
        owner = User.objects.get(id=user_id)
        owner_group, created = Group.objects.get_or_create(
            name=f'meetup-owner#{meetup_id}')
        owner_group.user_set.remove(owner)
    #     #TODO handle errors
        return redirect(f'/app/meetups/{meetup_id}/owner/')


@login_required()
@has_ownership
def event_index(request, meetup_id):
    logger.info(
        f"{request.method} request event index by user {request.user} meetup id {meetup_id}")

    meetup = Meetup.objects.get(id=meetup_id)
    events = Event.objects.filter(meetup=meetup_id)
    return render(request, 'app/events.html', {'meetup': meetup, 'events': events})


@login_required()
@has_ownership
def event_add(request, meetup_id):
    logger.info(
        f"{request.method} request event add by user {request.user} meetup id {meetup_id}")

    form = EventForm(request.POST or None)
    if form.is_valid():
        meetup = Meetup.objects.get(id=meetup_id)
        model = form.save(commit=False)
        channel_name = f'{str(model.name)}_{str(random.randint(0, 10000))}'
        model.channel = channel_name
        channel_created = chat.create_channel(channel_name)
        logger.info("Rocket channel created {}".format(channel_created))
        model.meetup = meetup
        model.status = Event.STATUS_CREATED
        model.save()
        return redirect(f'/app/meetups/{meetup_id}/events/')
    return render(request, 'app/event_add.html', {'form': form, 'meetup_id': meetup_id})


@login_required()
@has_ownership
def event_edit(request, meetup_id, event_id):
    logger.info(
        f"{request.method} request event edit by user {request.user} meetup id {meetup_id} event {event_id}")

    event = get_object_or_404(Event, pk=event_id)
    form = EventForm(request.POST or None, instance=event)

    if form.is_valid():
        form.save()
        return redirect(f'/app/meetups/{meetup_id}/events/')

    return render(request, 'app/event_edit.html', {"form": form, "meetup_id": meetup_id, "event": event})


@login_required()
@has_ownership
def event_delete(request, meetup_id, event_id):
    logger.info(
        f"{request.method} request event delete by user {request.user} meetup id {meetup_id} event {event_id}")

    event = get_object_or_404(Event, pk=event_id)
    form = EventDeleteForm(instance=event)

    if request.method == 'POST':
        event.delete()
        return redirect(f'/app/meetups/{meetup_id}/events/')

    return render(request, 'app/event_delete.html', {"form": form, "meetup_id": meetup_id, "event": event})


@login_required()
@has_ownership
def speaker_add(request, meetup_id, event_id):
    logger.info(
        f"{request.method} request speaker add by user {request.user} meetup id {meetup_id} event {event_id}")

    event = get_object_or_404(Event, pk=event_id)

    if request.method == 'POST':
        email = request.POST['speaker-email']
        speaker_user = User.objects.filter(email=email)

        # if username does not exists, add a temporary link to speaker email <-> event
        if speaker_user is None or len(speaker_user) == 0:
            inactive_speaker = models.InactiveSpeaker(
                event=event, speaker_email=email)
            inactive_speaker.save()
        else:
            speaker_group, created = Group.objects.get_or_create(
                name=f'event-speaker#{event_id}')
            speaker_group.user_set.add(speaker_user[0])

        return redirect(f'/app/meetups/{meetup_id}/events/{event_id}/speakers/')

    return render(request, 'app/speaker_add.html', {"meetup_id": meetup_id, "event_id": event_id})


@login_required()
@has_ownership
def speaker_index(request, meetup_id, event_id):
    logger.info(
        f"{request.method} request speaker index by user {request.user} meetup id {meetup_id} event {event_id}")

    if request.method == 'GET':
        event = get_object_or_404(Event, pk=event_id)

        all_speakers = []
        active_users = User.objects.filter(
            groups__name=f'event-speaker#{event_id}')
        inactive_users = models.InactiveSpeaker.objects.filter(event=event)

        all_speakers.extend(active_users)
        all_speakers.extend([User(email=u.speaker_email)
                             for u in inactive_users])

        return render(request, 'app/speakers.html', {'meetup_id': meetup_id, 'event_id': event_id, 'speakers': all_speakers})


@login_required()
@has_ownership
def speaker_delete(request, meetup_id, event_id, user_id):
    logger.info(
        f"{request.method} request speaker delete active by user {request.user} meetup id {meetup_id} event {event_id}")

    if request.method == 'GET':
        speaker = User.objects.get(id=user_id)
        speaker_group, created = Group.objects.get_or_create(
            name=f'event-speaker#{event_id}')
        speaker_group.user_set.remove(speaker)
    #     #TODO handle errors
        return redirect(f'/app/meetups/{meetup_id}/events/{event_id}/speakers/')


@login_required()
@has_ownership
def speaker_delete_inactive(request, meetup_id, event_id, email):
    logger.info(
        f"{request.method} request speaker delete inactive by user {request.user} meetup id {meetup_id} event {event_id} email {email}")

    if request.method == 'GET':
        event = get_object_or_404(Event, pk=event_id)
        event_speaker_mapping = models.InactiveSpeaker.objects.get(
            event=event, speaker_email=email)
        event_speaker_mapping.delete()

    #     #TODO handle errors
        return redirect(f'/app/meetups/{meetup_id}/events/{event_id}/speakers/')
