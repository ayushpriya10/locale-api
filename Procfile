web: gunicorn api.wsgi -b 0.0.0.0:$PORT --log-level debug
worker: celery -A api worker -l info --without-heartbeat