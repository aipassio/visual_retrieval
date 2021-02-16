#!/bin/bash
#install database
sudo apt-get install python-dev libpq-dev postgresql postgresql-contrib
sudo service postgresql restart
pip install virtualenv 
virtualenv -p python3 reid_env
source ./reid_env/bin/activate
pip install -r requirements.txt
source ./reid/db_configs.py
sudo -u postgres -H -- psql -c "DROP DATABASE IF EXISTS ${NAME};"
sudo -u postgres -H -- psql -c "CREATE DATABASE ${NAME};"
sudo -u postgres -H -- psql -d $NAME -c "CREATE EXTENSION IF NOT EXISTS hstore"
rm -r ./retrieval/migrations
python manage.py makemigrations
python manage.py migrate
python manage.py makemigrations retrieval
python manage.py migrate retrieval
python manage.py runserver