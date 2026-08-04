#!/bin/sh

# Wait for PostgreSQL if DB_HOST is set
if [ "$DB_HOST" = "db" ]; then
    echo "Waiting for PostgreSQL database..."
    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.5
    done
    echo "PostgreSQL started!"
fi

echo "Applying Django migrations..."
python backend/manage.py makemigrations
python backend/manage.py migrate

echo "Seeding database with MSU default test data..."
python backend/manage.py seed_db

exec "$@"
