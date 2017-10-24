from flask import current_app
from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

# AuctionSite table
class AuctionSite(db.Model):
	__tablename__ = 'auction_sites'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	wines = db.relationship('Listing', backref='auction_sites')

# Listing table
class Listing(db.Model):
	__tablename__ = 'listings'
	id = db.Column(db.Integer, primary_key=True)
	year = db.Column(db.Integer, index=True)
	producer = db.Column(db.String(64), index=True)
	alert = db.Column(db.String(64))
	price = db.Column(db.Float)
	old_price = db.Column(db.Float)
	time_added = db.Column(db.DateTime)
	time_removed = db.Column(db.DateTime)
	active = db.Column(db.Boolean)
	item_code = db.Column(db.String(32))
	site_id = db.Column(db.Integer, db.ForeignKey('auction_sites.id'))

# User table
class User(UserMixin, db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True, index=True)
	email = db.Column(db.String(64), unique=True, index=True)
	password_hash = db.Column(db.String(128))

	# True if user has clicked confirmation link, False otherwise
	confirmed = db.Column(db.Boolean, default=False)

	# Generates confirmation token using JSON Web Signature Serializer
	def generate_confirmation_token(self, expiration=3600):
		s = Serializer(current_app.config['SECRET_KEY'], expiration)
		return s.dumps({'confirm': self.id})

	# Confirms token's validity
	def confirm(self, token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except:
			return False
		if data.get('confirm') != self.id:
			return False
		self.confirmed = True
		db.session.add(self)
		return True

	@login_manager.user_loader
	def load_user(user_id):
		return User.query.get(int(user_id))

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return '<%r>' % self.username
		