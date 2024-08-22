FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install libpq-dev build-essential -y
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD celery -A starchat worker & gunicorn -c gunicorn.conf.py starchat.wsgi
