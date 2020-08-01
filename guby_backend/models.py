from django.db import models
from django.contrib import admin
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

'''
We can probably replace this using djano auth user group
'''

class GubyUser(AbstractUser):
    email = models.EmailField('email', db_index=True, unique=True)
    username = models.CharField('username', unique=False, default='NOUSER', max_length=10)
    name = models.CharField(max_length=50)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

class Roles(models.Model):
    name = models.TextField(unique=True)

class Meetup(models.Model):
    name = models.CharField(unique=True, max_length=200)
    description = models.CharField(max_length=1500)
    co_organizer_emails = models.CharField(max_length=300)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class Event(models.Model):
    name = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=1500, null=True)
    meetup = models.ForeignKey(Meetup, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    STATUS_ALL = 0
    STATUS_CREATED = 1
    STATUS_STARTED = 2
    STATUS_ENDED = 3

    STATUS_CHOICES = [
        (STATUS_ALL, 'ALL'),
        (STATUS_CREATED, 'CREATED'),
        (STATUS_STARTED, 'STARTED'),
        (STATUS_ENDED, 'ENDED'),
    ]

    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    lounges = models.TextField(default="")
    channels = models.TextField(default="")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class InactiveSpeaker(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    speaker_email = models.EmailField('email')

    class Meta:
        unique_together = ['event', 'speaker_email']