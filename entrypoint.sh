#!/bin/bash

echo "Waiting for postgres..."

while ! nc -z db 543w; do
	sleep 0.1
done

echo "PostgreSQL started"

python manage.py flush --no-input