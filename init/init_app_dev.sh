#!/bin/bash


flask db init
flask db upgrade
flask --debug run --host 0.0.0.0 