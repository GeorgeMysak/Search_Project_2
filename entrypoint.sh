#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z -v $SQL_HOST $SQL_PORT; do
    sleep 1
done

echo "PostgreSQL started"


exec "$@"