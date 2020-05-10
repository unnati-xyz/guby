#!/bin/sh
python manage.py makemigrations
python manage.py migrate
python manage.py makemigrations roles
python create_superuser.py 
exec python manage.py runserver 0.0.0.0:5000