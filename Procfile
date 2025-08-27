release: python manage.py migrate --noinput
web: gunicorn coresite.wsgi --bind 0.0.0.0:$PORT --workers 4
