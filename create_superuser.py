#!/usr/bin/env python
import django
django.setup()

from django.contrib.auth import get_user_model
import os
User = get_user_model()
User.objects.create_superuser(os.getenv('DJANGO_SU_NAME'), os.getenv('DJANGO_SU_EMAIL'), os.getenv('DJANGO_SU_PASSWORD'))