from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from guby_backend.models import InactiveSpeaker, Event

User = get_user_model()

@receiver(post_save, sender=User)
def lazy_save_speaker_user(sender, instance, **kwargs):
    event_user_mapping = InactiveSpeaker.objects.filter(speaker_email=instance.email)

    for row in event_user_mapping:
        event = row.event
        speaker_group, created = Group.objects.get_or_create(name=f'event-speaker#{event.id}')
        speaker_group.user_set.add(instance)
        row.delete()
    