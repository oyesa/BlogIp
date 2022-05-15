from flask import Flask
from config import config_options
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
# from flask_uploads import UploadSet, configure_uploads, IMAGES


#initialize extensions
db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()





# Initializing application
def create_app(config_name):
    app = Flask(__name__)
   
    

    #create app configurations
    app.config.from_object(config_options[config_name])

    #initialize the extensions
    bootstrap.init_app(app)
    db.init_app(app)
   


    #Register blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    

    return app