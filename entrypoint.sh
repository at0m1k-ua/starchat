#!/bin/bash

# Apply database migrations
python manage.py migrate

# Start Celery and Gunicorn
celery -A starchat worker & gunicorn -c gunicorn.conf.py starchat.wsgi
