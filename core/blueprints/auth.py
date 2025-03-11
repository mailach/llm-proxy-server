import logging
from functools import wraps

import flask
import flask_login

from werkzeug.security import check_password_hash 

from core import login_manager
from core.models import User
from core.forms import LoginForm


auth = flask.Blueprint("auth", __name__)


@login_manager.user_loader
def user_loader(user_id):
    return User.query.filter_by(id=user_id).first()


@login_manager.unauthorized_handler
def unauthorized_handler():
    return flask.redirect(flask.url_for("auth.login", next=flask.request.endpoint)) 



@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(id=username).first()

        if not user or not check_password_hash(user.pw_hash, password):
            flask.flash("Please check your login details and try again.", "danger")
        else:
            flask_login.login_user(user)
            logging.info("Successful login %r", user)
            flask.flash(f'Welcome, {username}!', 'success')
            return flask.redirect(flask.url_for('root.home'))  # Redirect to Flask-Admin or another page
    
    return flask.render_template('login.html', form=form)

  
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


