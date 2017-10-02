import os

# Absolute path to base directory of project
basedir = os.path.abspath(os.path.dirname(__file__))

# Base Application Configuration class
class Config:
	'''
	Base class for application configuration.
	Contains config variables that are common to all configurations
	'''
	SECRET_KEY = os.getenv('SECRET_KEY')
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SCRAPER_MAIL_SUBJECT_PREFIX = '[Wine Auction Aid]'
	SCRAPER_MAIL_SENDER = os.getenv('MAIL_SENDER')

	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	'''
	Configuration for development
	'''
	DEBUG = True
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.getenv('MAIL_USERNAME')
	MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
	SQLALCHEMY_DATABASE_URI =\
		'mysql+mysqlconnector://root:' + os.getenv('DB_PASS') + \
		'@localhost:3306/wine_scraper_devdb'

class TestingConfig(Config):
	'''
	Configuration for testing
	'''
	TESTING = True
	SQLALCHEMY_DATABASE_URI =\
		'mysql+mysqlconnector://root:' + os.getenv('DB_PASS') + \
		'@localhost:3306/wine_scraper_testdb'

class ProductionConfig(Config):
	'''
	Configuration for production
	'''
	SQLALCHEMY_DATABASE_URI =\
		'mysql+mysqlconnector://root:' + os.getenv('DB_PASS') + \
		'@localhost:3306/wine_scraper_db'

# Dictionary of configurations. Will be passed to Application Factory
config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,
	'default': DevelopmentConfig
}