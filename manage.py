from app import create_app,db
from flask_script import Manager,Server
from app.models import Role, User
from flask_migrate import Migrate, MigrateCommand



#Create app instance
app = create_app('production')

manager = Manager(app, db)
manager.add_command('server',Server)


manager.add_command("db", MigrateCommand) 
migrate = Migrate(app,db)  


@manager.shell
def make_shell_context():
   return dict(db = db, app = app, User = User, Role=Role)


@manager.command
def test():
    """
    Run the unit tests
    """
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    manager.run()

    

