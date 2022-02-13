import os
from decouple import config
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY=config('SECRET_KEY','Secret')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_SECRET_KEY = config('JWT_SECRET_KEY')

# development config
class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost/burgerzilla'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    DEBUG=config('DEBUG',cast=bool)

# test config
class TestConfig(Config):
    TESTING=True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

# production config
class ProdConfig(Config):
    pass

# config dictionary in order to access these classes from application factory.
config_dict = {
    "development":DevConfig,
    "production":ProdConfig,
    "testing":TestConfig
}