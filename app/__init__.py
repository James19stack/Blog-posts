from flask import Flask
from config import config_options
from flask_bootstrap import Bootstrap

def create_app(config_name):
    
    app=Flask(__name__)

    # Initializing Flask Extensions
    bootstrap = Bootstrap(app)

    #REGISTER CONFIGURATION
    app.config.from_object(config_options[config_name])

    from ..request import create_configuration
    create_configuration(app)


    return app
