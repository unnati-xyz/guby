#!/bin/sh
echo $INITIALIZE_DB
echo $INITIALIZE_APP_DB
if [ $INITIALIZE_DB == true ]
then
    echo "Initializing database for guby"
    python manage.py makemigrations 
    python manage.py migrate
    python create_superuser.py 
fi

if [ "$INITIALIZE_APP_DB" == "true" ]
then 
    echo "Initializing application database for guby"
    python manage.py makemigrations guby_backend 
    python manage.py migrate guby_backend 

fi

exec python manage.py runserver 0.0.0.0:5000