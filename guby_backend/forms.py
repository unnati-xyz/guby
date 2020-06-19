from django import forms
from django.forms import ModelForm

from .models import Meetup

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
            'name': forms.TextInput(attrs={'disabled': True}),
            'description': forms.Textarea(attrs={'disabled': True}),
            'co_organizer_emails': forms.Textarea(attrs={'disabled': True}),
        }

class MeetupEditForm(forms.Form):
   id = forms.IntegerField(widget=forms.HiddenInput)
   name = forms.CharField(label='Meetup Name', max_length=200)
   description = forms.CharField(label='Meetup Desc', max_length=3000)
   co_organizer_emails = forms.CharField(label='Co-organizers email id', widget=forms.Textarea)

class EventAddForm(forms.Form):
    start_date = forms.DateTimeField(label='Event Start Date Time')
    end_date = forms.DateTimeField(label='Event End Date Time')
    video_lounges = forms.CharField(max_length=500, initial='General,', label='Networking Lounges')
    chat_rooms = forms.CharField(max_length=500, initial='General,', label='Discussion Channel')

class EventDeleteForm(forms.Form):
    start_date = forms.DateTimeField(label='Event Start Date Time')
    start_date.disabled = True
    end_date = forms.DateTimeField(label='Event End Date Time')
    end_date.disabled = True
    video_lounges = forms.CharField(max_length=500, initial='General,', label='Networking Lounges')
    video_lounges.disabled = True
    chat_rooms = forms.CharField(max_length=500, initial='General,', label='Discussion Channel')
    chat_rooms.disabled = True