import os
import logging
import json

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from wtforms import StringField

import flask_login


from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.security import generate_password_hash

from logging.config import dictConfig

with open("config/logging_config.json", "r") as f:
    logging_config = json.load(f)

dictConfig(logging_config)


db = SQLAlchemy()
migrate = Migrate()
login_manager = flask_login.LoginManager()


# Postgres config
PG_PW = os.environ.get("POSTGRES_PASSWORD")
PG_USER = os.environ.get("POSTGRES_USER")
PG_DB = os.environ.get("POSTGRES_DB")
PG_HOST = os.environ.get("POSTGRES_HOST")
PG_PORT = os.environ.get("POSTGRES_PORT")

# Falls die Anwendung hinter einem Proxy mit Pfadweiterleitung läuft
PROXY_PATH_PREFIX = os.environ.get("PROXY_PATH_PREFIX")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Falls sachen nur in dev laufen sollen 
STAGE = os.environ.get("STAGE")


# app-factory
def create_app():
    app = Flask(__name__)
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = f"postgresql://{PG_USER}:{PG_PW}@{PG_HOST}:{PG_PORT}/{PG_DB}"
    app.config['JSON_AS_ASCII'] = False
    

    app.secret_key = os.environ.get("FLASK_SECRET_KEY")
    db.init_app(app)
    migrate.init_app(app, db)
    if PROXY_PATH_PREFIX:
        app.wsgi_app = ProxyFix(app.wsgi_app)
        
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='LLM Proxy', template_mode='bootstrap3')
    



    # Blueprint imports
    with app.app_context():
        
        
        from core.models import User
        from core.blueprints.root import root
        from core.blueprints.auth import auth
        
        

        
        
    class UserModelView(ModelView):
        page_size = 50 
        can_view_details = True
        column_list = (User.id, User.pw_hash)
        form_columns = ('id', 'pw_hash')
        
        form_extra_fields = {
        'id': StringField('ID')
         }
        
        def is_accessible(self):
            return True

        def on_model_change(self, form, model, is_created):
            if model.pw_hash:
                model.pw_hash = generate_password_hash(model.pw_hash)
        
    admin.add_view(UserModelView(User, db.session))

    login_manager.init_app(app)

    # Register imported blueprints
    app.register_blueprint(root)
    app.register_blueprint(auth)
    #app.register_blueprint(admin)

    return app
