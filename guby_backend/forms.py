from django import forms
from django.forms import ModelForm

from .models import Meetup, Event

class UserAddForm(forms.Form):
    name = forms.CharField(label='First & Last Name', max_length=50, required=True)
    email = forms.EmailField(label='Email Id', max_length=100, required=True)
    password = forms.CharField(max_length=32, label="Password", widget=forms.PasswordInput)
    repeat_password = forms.CharField(max_length=32, label="Repeat Password", widget=forms.PasswordInput)

class MeetupForm(ModelForm):
    class Meta:
        model = Meetup
        fields = ['name', 'description', 'co_organizer_emails']

class MeetupDeleteForm(ModelForm):
    class Meta:
        model = Meetup
        fields = ['name', 'description', 'co_organizer_emails']
        widgets = {
            'name': forms.TextInput(attrs={'disabledd': True}),
            'description': forms.Textarea(attrs={'disabledd': True}),
            'co_organizer_emails': forms.Textarea(attrs={'disabledd': True}),
        }

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['meetup', 'start_date', 'end_date', 'lounges', 'channels', 'status']

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

