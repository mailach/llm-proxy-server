import logging
import flask
from functools import wraps
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from wtforms import StringField
from werkzeug.security import generate_password_hash

from core.models import User

class RestrtrictedAdminView:
    def is_accessible(self):
        return current_user.id =="admin"  

    def inaccessible_callback(self, name, **kwargs):
        return flask.redirect(flask.url_for('auth.login')) 


class RestrictedIndexView(AdminIndexView):
    
    def is_accessible(self):
        return current_user.is_authenticated 
    
    def inaccessible_callback(self, name, **kwargs):
        return flask.redirect(flask.url_for('auth.login')) 

class UserModelView(RestrtrictedAdminView, ModelView):
        page_size = 50 
        can_view_details = True
        column_list = (User.id, User.pw_hash)
        form_columns = ('id', 'pw_hash')
        
        form_extra_fields = {
        'id': StringField('ID')
         }
        
        

        def on_model_change(self, form, model, is_created):
            if model.pw_hash:
                model.pw_hash = generate_password_hash(model.pw_hash)





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


