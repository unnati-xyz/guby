from django.db import models

# Create your models here.
'''
We can probably replace this using djano auth user group
'''
class Roles(models.Model):
    id = models.IntegerField(primary_key=True, db_column='id', auto_created=True)
    role_name = models.TextField(unique=True, db_column='role_name')

class Meetup(models.Model):
    id = models.IntegerField(primary_key=True, db_column='id', auto_created=True)
    name = models.TextField(unique=True, db_column='meetup_name')
    created_date = models.DateTimeField(db_column='created_date')
    updated_date = models.DateTimeField(db_column='updated_date')

class Event(models.Model):
    id = models.IntegerField(primary_key=True, db_column='id', auto_created=True)
    meetup_id = models.IntegerField()
    start_date = models.DateTimeField(db_column='start_date')
    end_date = models.DateTimeField(db_column='end_date')
    status = models.IntegerField(db_column='status')


