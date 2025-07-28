#!/bin/bash

echo "Aplicando migrações..."
python manage.py migrate

echo "Iniciando servidor Gunicorn..."
gunicorn loja_de_veiculos.wsgi:application --bind 0.0.0.0:$PORT
