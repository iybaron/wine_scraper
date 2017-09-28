import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	SECRET_KEY = os.getenv('SECRET_KEY')
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SCRAPER_MAIL_SUBJECT_PREFIX = '[Wine Auction Aid]'
	SCRAPER_MAIL_SENDER = os.getenv('MAIL_SENDER')

	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
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
	TESTING = True
	SQLALCHEMY_DATABASE_URI =\
		'mysql+mysqlconnector://root:' + os.getenv('DB_PASS') + \
		'@localhost:3306/wine_scraper_testdb'

class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI =\
		'mysql+mysqlconnector://root:' + os.getenv('DB_PASS') + \
		'@localhost:3306/wine_scraper_db'

config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,
	'default': DevelopmentConfig
}