FROM python:3.7-alpine
WORKDIR /code
RUN apk add --no-cache gcc musl-dev linux-headers postgresql-dev

COPY . .
RUN chmod +x /code/create_superuser.py
RUN pip install -r requirements.txt
RUN chmod +x /code/guby_initialize.sh
ENTRYPOINT ["/code/guby_initialize.sh"]
