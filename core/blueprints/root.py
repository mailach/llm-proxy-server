import flask
# so sehen imports aus der eigenen Anwendung aus, immer absolute pfade nehmen

# from core import db
# from core.blueprints.auth import access_with_api_key
# from core.blueprints.admin import access_only_admin


root = flask.Blueprint("root", __name__)

@root.route("/")
def index():
    return flask.render_template("hellow_world.html")