import os
from app import create_app, db
from app.models import User
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

# Call application factory function with given configuration
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

# Manager provides command line interaction with application
manager = Manager(app)
migrate = Migrate(app, db)

# Provide shell interaction with app context
def make_shell_context():
	return dict(app=app, db=db, User=User)
manager.add_command('shell', Shell(make_context=make_shell_context))

# Provides easy command line database migration
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
	manager.run()