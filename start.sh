#!/bin/bash
# Script de démarrage pour le déploiement
echo "Démarrage du projet Stage Hub..."
cd plateforme_stage
export DJANGO_SETTINGS_MODULE=config.settings.production
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn config.wsgi --bind 0.0.0.0:$PORT
