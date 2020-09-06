import logging
from functools import wraps
from django.http import HttpResponseForbidden
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)

def has_ownership(func):
    
    @wraps(func)
    def check_owner_wrapper(request, *args, **kwargs):
        meetup_id = kwargs['meetup_id']
        if request.user.is_authenticated and request.user.groups.filter(name=f'meetup-owner#{meetup_id}').exists():

            return func(request, *args, **kwargs)

        else:
            return HttpResponseForbidden()
    
    return check_owner_wrapper

def get_own_meetup_ids(user):
    logger.info(f"get own meetups for user {user}")
    # get group names where the user is owner
    group_names = user.groups.all()

    # extract meetup id from group name
    meetup_ids = []
    for g in group_names:
        if g.name.startswith('meetup-owner'):
                meetup_ids.append(g.name.split('#')[1])

    return meetup_ids


def create_inactive_user(email):
    logger.info(f"create inactive user {email}")
    User = get_user_model()
    new_user = User(email=email, name=email, is_active=False)
    new_user.save()
    return new_user
