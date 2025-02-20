# 3rd-party packages
from flask import Flask, render_template, request, redirect, url_for
from flask_mongoengine import MongoEngine
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)
import os

# Local
from .client import CityClient, WeatherClient

# Clients
db = MongoEngine()
login_manager = LoginManager()
bcrypt = Bcrypt()
city_client = CityClient()
weather_client = WeatherClient()

# Blueprints
from .weather.routes import weather
from .users.routes import users


def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_pyfile("config.py", silent=False)
    if test_config is not None:
        app.config.update(test_config)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(weather)
    app.register_blueprint(users)

    login_manager.login_view = "users.login"

    return app
