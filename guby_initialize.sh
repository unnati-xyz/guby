#!/bin/sh

set -e

# Get host:port from parameters list
host="db"
echo "###########----##########";
echo $host;
echo "###########----##########";
# Try to connect to PostgreSQL
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$host" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

echo "Postgres is up - executing command"

echo "###########----##########";
echo "$INITIALIZE_DB"
echo "$INITIALIZE_APP_DB"
echo "###########----##########";
if [ "$INITIALIZE_DB" == true ]
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