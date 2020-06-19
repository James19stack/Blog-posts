import os
class Config:
    SECRET_KEY=os.environ.get('SECRET_KEY')
    RANDOM_API='http://quotes.stormconsultancy.co.uk/random.json'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://jefferson:james_22@localhost/watchlist'

class ProdConfig(Config):
    pass

class DevConfig(Config):
    DEBUG=True

config_options={
    'development':DevConfig,
    'production':ProdConfig
}    