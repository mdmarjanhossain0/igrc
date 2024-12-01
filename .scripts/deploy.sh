#!/bin/bash
set -e

echo "Deployment started ..."

git pull origin master
echo "New changes copied to server !"

source ../venv/bin/activate
echo "Virtual env Activated !"

echo "Installing Dependencies..."
pip3 install -r requirements.txt --no-input

# echo "Serving Static Files..."
# python manage.py collectstatic --noinput

echo "Running Database migration"
python3 manage.py makemigrations
python3 manage.py migrate

deactivate
echo "Virtual env Deactivated !"

pushd mysite
touch asgi.py
popd

sudo systemctl restart grc

echo "Deployment Finished!"

# git update-index --add --chmod=+x deploy.sh