"""Flask config class."""
import os
from datetime import timedelta

class BaseConfig:
    """Base config vars."""
    DEBUG=True
    SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True
    SECRET_KEY = os.environ.get('SECRET_KEY')

    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=10)
    
