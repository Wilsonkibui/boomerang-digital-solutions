#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

# Skip migrations for now to test if database connection is the issue
# python manage.py migrate
