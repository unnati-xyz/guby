from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from guby_backend.models import *
from guby_backend.forms import GubyUserCreationForm, GubyUserChangeForm

User = get_user_model()

class GubyUserAdmin(UserAdmin):
    add_form = GubyUserCreationForm
    form = GubyUserChangeForm
    model = GubyUser
    list_display = ['email', 'name']

# Register your models here.
admin.site.register(Meetup)
admin.site.register(Event)
# admin.site.register(Speaker)
admin.site.register(GubyUser, GubyUserAdmin)
