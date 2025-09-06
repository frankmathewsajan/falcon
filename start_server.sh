#!/bin/bash

# Falcon Django App Startup Script

echo "Starting Falcon Django Application..."

# Activate virtual environment
source .venv/bin/activate

# Install/update dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo "Running database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start Gunicorn with configuration
echo "Starting Gunicorn server..."
gunicorn -c gunicorn_config.py falcon.wsgi:application

echo "Falcon application started successfully!"
