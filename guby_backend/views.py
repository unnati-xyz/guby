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

