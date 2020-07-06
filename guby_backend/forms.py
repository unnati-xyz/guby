from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from bootstrap_datepicker_plus import DatePickerInput

from .models import Meetup, Event

User = get_user_model()
class GubyUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'name',]

class GubyUserChangeForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'name',]

class MeetupForm(ModelForm):
    class Meta:
        model = Meetup
        fields = ['name', 'description', 'co_organizer_emails']
        widgets = {
           'co_organizer_emails': forms.Textarea(attrs={'disabled': False,})
        }

class MeetupDeleteForm(ModelForm):
    class Meta:
        model = Meetup
        fields = ['name', 'description', 'co_organizer_emails']
        widgets = {
            'name': forms.TextInput(attrs={'disabled': True}),
            'description': forms.Textarea(attrs={'disabled': True}),
            'co_organizer_emails': forms.Textarea(attrs={'disabled': True}),
        }

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'start_date', 'end_date', 'lounges', 'channels']
        widgets = {
            'start_date' : DatePickerInput(format='%Y-%m-%d'),
            'end_date' : DatePickerInput(format='%Y-%m-%d'),
            'lounges' : forms.TextInput(),
            'channels' : forms.TextInput(),
            'name' : forms.TextInput(),
            'description' : forms.Textarea()
        }

class EventDeleteForm(ModelForm):
    class Meta:
        model = Event
        fields = ['meetup', 'start_date', 'end_date', 'lounges', 'channels', 'status']
        widgets = {
            'meetup': forms.TextInput(attrs={'disabled': True}),
            'start_date': forms.TextInput(attrs={'disabled': True}),
            'end_date': forms.TextInput(attrs={'disabled': True}),
            'lounges': forms.TextInput(attrs={'disabled': True}),
            'channels': forms.TextInput(attrs={'disabled': True}),
            'status': forms.TextInput(attrs={'disabled': True}),
        }

