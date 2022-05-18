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
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL").replace("postgres://", "postgresql://", 1)
    
  
    

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://oyesa:crowne@localhost/blogip_test'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://oyesa:crowne@localhost/blogip'


class DevConfig(Config):


    DEBUG = True


config_options = {
    "test": TestConfig,
    "production": ProdConfig,
    "development": DevConfig
} 