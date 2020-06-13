from django import forms

class MeetupAddForm(forms.Form):
    name = forms.CharField(label='Meetup Name', max_length=500)
    description = forms.CharField(label='Meetup Desc', max_length=3000)
    coorganize_email_id = forms.CharField(label='Co-organizers email id', max_length=1000)