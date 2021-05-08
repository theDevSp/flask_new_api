from .PROD_config import ProductionConfig
from .DEV_config import DevelopmentConfig

configurations = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
