web: sh -c "python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn coresite.wsgi:application --bind 0.0.0.0:$PORT"
