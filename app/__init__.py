from flask import Flask
from config import config_options
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy


bootstrap = Bootstrap()
db = SQLAlchemy()


def create_app(config_name):
    
    app=Flask(__name__)

    # Initializing Flask Extensions
    bootstrap = Bootstrap(app)
    db.init_app(app)

    # Registering the blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    #REGISTER CONFIGURATION
    app.config.from_object(config_options[config_name])

    from ..request import create_configuration
    create_configuration(app)


    return app
