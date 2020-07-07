from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('users/', include('django.contrib.auth.urls')),
    path('users/signup/', views.SignUpView.as_view(), name='signup'),
    path('meetups/', views.meetup_index, name='meetup_index'),
    path('meetups/add/', views.meetup_add, name='meetup_add'),
    path('meetups/<int:meetup_id>/edit/', views.meetup_edit, name='meetup_edit'),
    path('meetups/<int:meetup_id>/delete/', views.meetup_delete, name='meetup_delete'),
    path('meetups/<int:meetup_id>/owner/', views.meetup_owner_add, name='meetup_owner_add'),
    path('meetups/<int:meetup_id>/events/', views.event_index, name='event_index'),
    path('meetups/<int:meetup_id>/events/add/', views.event_add, name='event_add'),
    path('meetups/<int:meetup_id>/events/<int:event_id>/edit/', views.event_edit, name='event_edit'),
    path('meetups/<int:meetup_id>/events/<int:event_id>/delete/', views.event_delete, name='event_delete'),
]