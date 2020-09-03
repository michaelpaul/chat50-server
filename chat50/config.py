import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '..', '.env'))


class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    REDIS_URL = os.getenv('REDIS_URL')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    CORS_ALLOWED_ORIGINS = ['http://localhost:3000']

    # API Auth
    AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
    API_IDENTIFIER = os.getenv("API_IDENTIFIER")
    JWT_ALGORITHMS = ["RS256"]


class Testing(Config):
    ENV = 'development'
    TESTING = True
    REDIS_URL = None


class Development(Config):
    ENV = 'development'
    DEBUG = True
    SQLALCHEMY_ECHO = True


class Production(Config):
    ENV = 'production'
    CORS_ALLOWED_ORIGINS = ['https://chat50.netlify.app']
