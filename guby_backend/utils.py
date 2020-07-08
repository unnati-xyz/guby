from functools import wraps
from django.http import HttpResponseForbidden

def has_ownership(func):
    
    @wraps(func)
    def check_owner_wrapper(request, *args, **kwargs):
        meetup_id = kwargs['meetup_id']
        if request.user.is_authenticated and request.user.groups.filter(name=f'guby-meetup-{meetup_id}-owners').exists():

            return func(request, *args, **kwargs)

        else:
            return HttpResponseForbidden()
    
    return check_owner_wrapper


