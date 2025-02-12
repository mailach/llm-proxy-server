import os
import json

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
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

# bei ersten startup will man eigentlich einen Adminuser mit Adminpasswort erstellen... 
ADMIN_PW = os.environ.get("ADMIN_PW")

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

    # Blueprint imports
    with app.app_context():
        from core.blueprints.root import root
        from core.blueprints.auth import auth
        from core.blueprints.admin import admin

    login_manager.init_app(app)

    # Register imported blueprints
    app.register_blueprint(root)
    app.register_blueprint(auth)
    app.register_blueprint(admin)

    return app
