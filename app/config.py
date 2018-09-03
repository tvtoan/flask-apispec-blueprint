import os

class BaseConfig:
    """
    Base application configuration
    """
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'a9ab993c2e0a150c1d4bf061721bd1d7')


class DevelopmentConfig(BaseConfig):
    """
    Development application configuration
    """
    DEBUG = True
    MONGO_URI = 'mongodb://aicrawler.info:27017/account'