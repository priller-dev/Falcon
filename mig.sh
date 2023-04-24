#!/bin/bash

./manage.py makemigrations
./manage.py migrate
./manage.py loaddata categories