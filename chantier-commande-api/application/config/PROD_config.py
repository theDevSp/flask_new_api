"""Flask config class."""
import os
from .base_config import BaseConfig

class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False
    DB_URL = os.environ.get('DB_URL_PROD')
    DB_NAME = os.environ.get('DB_NAME_PROD')
    ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY_PROD')
    JWT_SECRET_KEY = os.environ.get('SECRET_KEY_PROD')