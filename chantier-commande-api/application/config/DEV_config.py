"""Flask config class."""
import os
from .base_config import BaseConfig


class DevelopmentConfig(BaseConfig):

    ODOO_URL = os.environ.get('ODOO_URL_DEV')
    DB_URL = os.environ.get('DB_URL_DEV')
    DB_NAME = os.environ.get('DB_NAME_DEV')
    ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY_DEV')
    JWT_SECRET_KEY = os.environ.get('SECRET_KEY_DEV')

    DB_CREDENTIAL = os.environ.get('DB_CREDENTIAL_DEV')

