#!/bin/sh

# Espera o banco PostgreSQL ficar disponível
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; do
  echo "Postgres não está pronto. Aguardando..."
  sleep 2
done

echo "Postgres está pronto!"

# Cria migrations de TODOS os apps (opcional, mas garante que não esquece nada)
python manage.py makemigrations

# Aplica TODAS as migrations no banco
python manage.py migrate --noinput

# Inicia Gunicorn
gunicorn aluconnect.wsgi:application --bind 0.0.0.0:8000 --workers 3
