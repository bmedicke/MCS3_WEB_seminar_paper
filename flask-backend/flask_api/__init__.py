from dotenv import load_dotenv  # automatically load .flaskenv
from flask import Flask
from flask_wtf.csrf import CSRFProtect
import os


def create_app(test_config=None):
    """
    application factory function for the Flask app.

    returns a Flask object
    """
    # create a flask instance with config files relative to this file:
    # TODO SECRET_KEY should be overwritten with a random value when deploying!
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
        DATABASE=os.path.join(app.instance_path, "flask-api.sqlite"),
    )

    if test_config is None:
        # load app config:
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load test config:
        app.config.from_mapping(test_config)

    # create instance folder for the sqlite db (if it's not already existing):
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # register database functions with the app:
    from . import database

    database.init_app(app)

    # register authentication blueprint:
    from . import auth

    app.register_blueprint(auth.blueprint)

    # register profile blueprint:
    from . import profile

    app.register_blueprint(profile.blueprint)

    # register message blueprint (including index endpoint):
    from . import message

    app.register_blueprint(message.blueprint)
    app.add_url_rule("/", endpoint="index")

    csrf = CSRFProtect()
    csrf.init_app(app)
    return app
