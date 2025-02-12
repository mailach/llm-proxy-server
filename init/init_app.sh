#!/bin/bash
flask db upgrade
SCRIPT_NAME=/path_to_app gunicorn --config config/gunicorn_config.py wsgi:app
