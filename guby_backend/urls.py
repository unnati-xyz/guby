from django.urls import path

from . import views

urlpatterns = [
    path('speakers', views.speaker_index, name='speaker_index'),
    path('speakers/add/', views.speaker_add, name='speaker_add'),
    path('meetup/add/', views.meetup_add, name='meetup_add'),
    path('event/add/', views.event_add, name='event_add'),
]