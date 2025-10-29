import os

class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    DEBUG = True
    CACHE_TYPE =  "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 300
