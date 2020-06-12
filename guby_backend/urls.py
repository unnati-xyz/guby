from django.urls import path

from . import views

urlpatterns = [
    path('speakers', views.speaker_index, name='speaker_index'),
    path('speakers/add/', views.speaker_add, name='speaker_add'),
    path('meetups', views.meetup_index, name='meetup_index'),
    path('meetup/1', views.meetup_desc, name='meetup_desc'),
    path('meetup/add/', views.meetup_add, name='meetup_add'),
    path('meetup/1/edit', views.meetup_edit, name='meetup_edit'),
    path('event/add/', views.event_add, name='event_add'),
]