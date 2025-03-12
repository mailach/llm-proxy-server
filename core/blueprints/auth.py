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
            return flask.redirect('/')  
    
    return flask.render_template('login.html', form=form)

  
@auth.route("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for("auth.login")) 


def _extract_api_key(header):
    if not header:
        return 'No api-key passed in the Authorization header'
    
    return header.replace("Bearer", "")
    
    

def api_key_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):
    api_key = None

    if 'Authorization' in flask.request.headers:
        api_key = _extract_api_key(flask.request.headers['Authorization'])

    user = User.query.filter_by(api_key=api_key.strip()).first()

    if not user:
        return 'Invalid token'

    return f(user, *args, **kwargs)
   
   return decorator


