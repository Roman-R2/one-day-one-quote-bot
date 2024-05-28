#!/bin/sh
echo "Into entrypoint.sh..."

if [ "$DATABASE" = "postgres" ]; then

  echo "Waiting for postgres..."

  while ! nc -z "$DB_HOST" "$DB_PORT"; do
    sleep 0.1
  done

  echo "PostgreSQL started"

fi

alembic upgrade $ALEMBIC_START_REVISION_ID

python3 main.py

exec "$@"
