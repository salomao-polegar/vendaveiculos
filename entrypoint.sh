#!/bin/bash

echo "Aplicando migrações..."
python manage.py migrate

echo "Iniciando servidor Gunicorn..."
gunicorn projeto.wsgi:application --bind 0.0.0.0:$PORT
