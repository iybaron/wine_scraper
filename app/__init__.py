from flask import flask, render_template
from flask_bootstrap import Bootstrap
from flas_sqlalchemy import SQLAlchemy
from config import config
from main import main_blueprint
from auth import auth_blueprint

bootstrap = Bootstrap()
mail = Mail()
db = SQLAlchemy()

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)

	bootstrap.init_app(app)
	mail.init_app(app)
	db.init_app(app)
	app.register_blueprint(main_blueprint)
	app.register_blueprint(auth_blueprint)
	
	return app