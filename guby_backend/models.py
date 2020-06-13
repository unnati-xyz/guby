from django.db import models
from django.contrib import admin

# Create your models here.
'''
We can probably replace this using djano auth user group
'''
class Roles(models.Model):
    name = models.TextField(unique=True)

class Meetup(models.Model):
    name = models.TextField(unique=True)
    description = models.TextField()
    co_organizer_emails = models.TextField()
    #owner = models.ForeignKey('auth_user', on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class Event(models.Model):
    meetup = models.ForeignKey(Meetup, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class Speaker(models.Model):
    name = models.TextField()
    email = models.EmailField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
