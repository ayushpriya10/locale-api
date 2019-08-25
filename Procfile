web: gunicorn api.wsgi -b 0.0.0.0:$PORT --log-level debug -t 3600
worker: celery -A api worker -l info -c 4 --without-heartbeat