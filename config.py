import os
class Config:
    SECRET_KEY=os.environ.get('SECRET_KEY')
    RANDOM_API='http://quotes.stormconsultancy.co.uk/random.json'

class ProdConfig(Config):
    pass

class DevConfig(Config):
    DEBUG=True

Config_options={
    'development':DevConfig,
    'production':ProdConfig
}    