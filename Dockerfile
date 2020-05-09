FROM python:3.7-alpine
WORKDIR /code
RUN apk add --no-cache gcc musl-dev linux-headers postgresql-dev

COPY requirements.txt requirements.txt
COPY guby/ /code/guby
COPY requirements.txt .
COPY manage.py .
COPY guby_initialize.sh /code/
COPY create_superuser.py /code/
RUN chmod +x /code/guby_initialize.sh
RUN chmod +x /code/create_superuser.py
RUN pip install -r requirements.txt

ENV DB_HOST='db'
ENV DJANGO_DB_NAME=guby
ENV DJANGO_SU_NAME=guby_admin
ENV DJANGO_SU_EMAIL=admin@my.company
ENV DJANGO_SU_PASSWORD=abcd1234
ENTRYPOINT ["/code/guby_initialize.sh"]
