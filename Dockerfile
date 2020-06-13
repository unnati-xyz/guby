FROM python:3.7-alpine
WORKDIR /code
RUN apk add --no-cache gcc musl-dev linux-headers postgresql-dev postgresql-client

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
ENTRYPOINT ["/code/guby_initialize.sh"]
