import os
import json

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin


import flask_login


from werkzeug.middleware.proxy_fix import ProxyFix

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
    app.config["PROXY_PATH_PREFIX"] = PROXY_PATH_PREFIX
    

    app.secret_key = os.environ.get("FLASK_SECRET_KEY")
    db.init_app(app)
    migrate.init_app(app, db)
    if PROXY_PATH_PREFIX:
        app.wsgi_app = ProxyFix(app.wsgi_app)
        
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    

    with app.app_context():
        
        
        from core.admin import RestrictedIndexView, UserModelView, LanguageModelView
        from core.models import User, LanguageModel
        from core.blueprints.auth import auth
        from core.blueprints.completions import completions
        
    admin = Admin(app, name='SWS LLM Self-Service', template_mode='bootstrap4', index_view=RestrictedIndexView())
    admin.add_view(UserModelView(User, db.session))
    admin.add_view(LanguageModelView(LanguageModel, db.session))
    
    login_manager.init_app(app)

    # Register imported blueprints
    app.register_blueprint(auth)
    app.register_blueprint(completions)

    return app
