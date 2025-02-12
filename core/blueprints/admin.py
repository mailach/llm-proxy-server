import json
import logging
from functools import wraps

import flask
import flask_login

# from werkzeug.security import generate_password_hash <- eine Möglichkeit passwort hashes zu generieren die dann in der DB gespeichert werden

from core.models import User
from core import PROXY_PATH_PREFIX

admin = flask.Blueprint("admin", __name__)


# Decorator um Endpunkte nur für Admins zugänglich zu machen
def access_only_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        # Logik um zu überprüfen ob aktueller User Adminrechte hat (dummy code)
        current_user_admin = True 
        if current_user_admin:
            return func(*args, **kwargs)
        else:
        # Redirect, error handling o.ä.
            return 405, "Not allowed"

    return wrapper


@admin.route("/admin", methods=["GET"])
@flask_login.login_required
@access_only_admin
def administration():
    # eine Möglichkeit das Admin board zu erstellen, alternativ flask-admin oder ähnliches
    return # flask.render_template() <- Admin template

