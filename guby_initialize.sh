#!/bin/sh
RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python create_superuser.py 
exec python manage.py runserver 0.0.0.0:5000