#!/usr/bin/env python
import django
django.setup()

from django.contrib.auth.models import User
import os
User.objects.create_superuser(os.getenv('DJANGO_SU_NAME'), os.getenv('DJANGO_SU_EMAIL'), os.getenv('DJANGO_SU_PASSWORD'))