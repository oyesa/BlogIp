import os 

class Config:
    '''
    General configuration parent class
    '''
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://oyesa:crowne@localhost/blogip'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOADED_PHOTOS_DEST = 'app/static/photos'

    @staticmethod
    def init_app(app):
        pass
       

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