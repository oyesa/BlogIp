import os

class Config:
    '''
    General configuration parent class
    '''
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://oyesa:Mimo33@localhost/blogdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
       

class ProdConfig(Config):
    pass
  
    

class TestConfig(Config):
   pass


class DevConfig(Config):


    DEBUG = True


config_options = {
    "test": TestConfig,
    "production": ProdConfig,
    "development": DevConfig
} 