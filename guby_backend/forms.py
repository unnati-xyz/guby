from django import forms

class UserAddForm(forms.Form):
    name = forms.CharField(label='First & Last Name', max_length=50, required=True)
    email = forms.EmailField(label='Email Id', max_length=100, required=True)
    password = forms.CharField(max_length=32, label="Password", widget=forms.PasswordInput)
    repeat_password = forms.CharField(max_length=32, label="Repeat Password", widget=forms.PasswordInput)

class MeetupAddForm(forms.Form):
    name = forms.CharField(label='Meetup Name', max_length=500)
    description = forms.CharField(label='Meetup Desc', max_length=3000)
    coorganize_email_id = forms.CharField(label='Co-organizers email id', max_length=1000)

class MeetupDeleteForm(forms.Form):
    name = forms.CharField(label='Meetup Name', max_length=500)
    name.disabled = True
    description = forms.CharField(label='Meetup Desc', max_length=3000)
    description.disabled = True
    coorganize_email_id = forms.CharField(label='Co-organizers email id', max_length=1000)
    coorganize_email_id.disabled = True

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