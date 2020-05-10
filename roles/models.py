from django.db import models

# Create your models here.
class Roles(models.Model):
    id = models.IntegerField(primary_key=True, db_column='id', auto_created=True)
    role_name = models.TextField(unique=True, db_column='role_name')
