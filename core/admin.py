import flask
import uuid
from functools import wraps
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from wtforms import StringField, FloatField
from wtforms.validators import InputRequired

from werkzeug.security import generate_password_hash

from core.models import User, LanguageModel

class RestrtrictedAdminView:
    def is_accessible(self):
        return current_user.id =="admin"  

    def inaccessible_callback(self, name, **kwargs):
        return flask.redirect(flask.url_for('auth.login')) 


class RestrictedIndexView(AdminIndexView):
    def __init__(self, **kwargs):
        super().__init__(url="/", **kwargs) 
        
    @expose('/')
    def index(self):
        completion_models = [u.__dict__ for u in LanguageModel.query.all()]

        return self.render('home.html', username=current_user.id, budget=current_user.budget, used_budget=current_user.used_budget, api_key=current_user.api_key, completion_models=completion_models)
    
    def is_visible(self):
        return False
    
    
    def is_accessible(self):
        return current_user.is_authenticated 
    
    def inaccessible_callback(self, name, **kwargs):
        return flask.redirect(flask.url_for('auth.login')) 
    
    
    


class UserModelView(RestrtrictedAdminView, ModelView):
    page_size = 50
    can_view_details = True
    can_edit = True
    column_list = (User.id, User.budget, User.used_budget, User.api_key)
    
    form_columns = ('id', 'password', 'budget', 'used_budget')  
    
    form_extra_fields = {
        'id': StringField('ID', validators=[InputRequired()]),
        'password': StringField('Password'),  
        'budget': FloatField('Budget', validators=[InputRequired()], default=5),
        'used_budget': FloatField('Used budget', default=0)
    }
    

    def on_model_change(self, form, model, is_created):
        if form.password.data:  
            model.pw_hash = generate_password_hash(form.password.data)
            
        if is_created:
            model.api_key = uuid.uuid4()
        else:
            model.id = model.id
            
        


class LanguageModelView(RestrtrictedAdminView, ModelView):
    page_size = 50
    can_view_details = True
    can_edit = True
    column_list = (LanguageModel.name, LanguageModel.encoding_model, LanguageModel.provider, LanguageModel.price_input_token, LanguageModel.price_output_token )
    
    form_columns = ('name', 'encoding_model', 'provider', 'price_input_token', 'price_output_token')  
    
    form_extra_fields = {
        'name': StringField('Name', validators=[InputRequired()]),
        'encoding_model': StringField('Encoding model', validators=[InputRequired()]),  
        'provider': StringField('Provider', validators=[InputRequired()]),
        'price_input_token': FloatField('Pricing 1M input token ($)', validators=[InputRequired()], default=0),
        'price_output_token': FloatField('Pricing 1M output token ($)', validators=[InputRequired()], default=0)
    }
    
    def on_model_change(self, form, model, is_created):
            
        if is_created:
            model.api_key = uuid.uuid4()
        else:
            model.id = model.id





