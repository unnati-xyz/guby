from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from roles.models import Roles


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


