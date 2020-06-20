from app import create_app,db
from flask_script import Server,Manager
from app.models import User
from flask_migrate import Migrate,MigrateCommand

app=create_app('test')
manager=Manager(app)
migrate = Migrate(app,db)

manager.add_command('db',MigrateCommand)
manager.add_command('server',Server)

@manager.shell
def make_shell_context():
    return dict(app = app,db = db,User = User)

@manager.command
def test():
    import unittest
    test=unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(test)   

if __name__=='__main__':
    manager.run()    