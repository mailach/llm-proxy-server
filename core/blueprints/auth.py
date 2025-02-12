import logging
from functools import wraps

import flask
import flask_login


# from werkzeug.security import check_password_hash <- eine Möglichkeit passwort hashes zu vergleichen

# from core.models import User <- Import aller relevanter Datentypen

from core import login_manager

auth = flask.Blueprint("auth", __name__)


@login_manager.user_loader
def user_loader(user_id):
    return # User.query.filter_by(id=user_id).first() <- abhängig vom Datenmodell


@login_manager.unauthorized_handler
def unauthorized_handler():
    return # flask.redirect(flask.url_for("auth.login", next=flask.request.endpoint)) <- Weiterleitung wenn auf unberechtigte Seite zugegriffen wird


@auth.route("/login", methods=["GET", "POST"])
def login():
    if flask.request.method == "GET":
        return # flask.render_template("login.html") <- z.B wenn auf eine login page weitergeleitet werden soll


    # Beispiel Login, hängt vom Datenmodell ab

    # user_id = flask.request.form["name"]
    # password = flask.request.form["pw"]

    # user = User.query.filter_by(id=user_id).first()

    # if not user or not check_password_hash(user.password, password):
    #     flask.flash("Please check your login details and try again.")
    #     return "Bad Login"

    # flask_login.login_user(user)
    # logging.info("Successful login %r", user)

    return # flask.redirect(flask.url_for()) <- hier dann landing page nach login eintragen


@auth.route("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return # flask.redirect(flask.url_for("auth.login")) <- redirect nach logout




# Decorator um Endpunkte nur mit API access zugänglich zu machen
def access_with_api_key(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # hier die Logik programmieren wie API keys authorisiert werden. 
        # if erfolgreiche authorisierung: 
        api_key_valid = True
        if api_key_valid: 
            return func(*args, **kwargs)
        else:
        # Redirect, error handling o.ä.
            return 405, "Not allowed"
    return wrapper