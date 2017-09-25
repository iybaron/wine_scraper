import os

basedir = os.path.apspath(os.path.dirname(__file__))

class Config:
	SECRET_KEY = os.environ['SECRET_KEY']
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True

	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI =\
		'mysql+mysqlconnector://root:' + os.environ.get('DB_PASS') + \
		'@localhost:3306/wine_scraper_devdb'

class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI =\
		'mysql+mysqlconnector://root:' + os.environ.get('DB_PASS') + \
		'@localhost:3306/wine_scraper_testdb'

class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI =\
		'mysql+mysqlconnector://root:' + os.environ.get('DB_PASS') + \
		'@localhost:3306/wine_scraper_db'

config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,
	'default': DevelopmentConfig
}