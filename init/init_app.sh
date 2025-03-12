#!/bin/bash
flask db upgrade
SCRIPT_NAME=/sws-llm-proxy gunicorn --config config/gunicorn_config.py wsgi:app
