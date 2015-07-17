#!/usr/bin/env bash

docker-compose run web nosetests -v --with-coverage --cover-erase --cover-package=app --cover-xml --cover-html
