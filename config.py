import os
class Config:
    SECRET_KEY=os.environ.get('SECRET_KEY')
    RANDOM_API='http://quotes.stormconsultancy.co.uk/random.json'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://jefferson:james_22@localhost/blogposts'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    #  email configurations
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL=True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
class ProdConfig(Config):
    pass

class DevConfig(Config):
    DEBUG=True

config_options={
    'development':DevConfig,
    'production':ProdConfig
}    