import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '..', '.env'))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    # API Auth
    AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
    API_IDENTIFIER = os.getenv("API_IDENTIFIER")
    JWT_ALGORITHMS = ["RS256"]
