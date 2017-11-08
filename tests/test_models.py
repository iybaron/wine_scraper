import unittest
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app import create_app, db
from app.models import User


class UserTestCase(unittest.TestCase):
	def setUp(self):
		self.app = create_app('testing')
		self.app_context = self.app.app_context()
		self.app_context.push()
		db.create_all()
		user1 = User(email='user1@email.com', username='John Doe', \
					 password='Cat')
		user2 = User(email='user2@email.com', username='Jane Doesworth', \
					 password='Dog')
		db.session.add(user1)
		db.session.add(user2)
		db.session.commit()

	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()

	def test_password_privacy(self):
		user = db.session.query(User).first()
		with self.assertRaises(AttributeError):
			user.password

	def test_generate_token(self):
		user = db.session.query(User).\
			   filter(User.username == 'John Doe').first()
		token = user.generate_confirmation_token()
		s = Serializer(current_app.config['SECRET_KEY'], 3600)
		data = s.loads(token)
		self.assertIsInstance(data, dict)
		self.assertEqual(data['confirm'], user.id)
	
	def test_confirm_bad_token(self):
		user1 = db.session.query(User).\
			    filter(User.username == 'John Doe').first()
		user2 = db.session.query(User).\
			    filter(User.username == 'Jane Doesworth').first()
		token = user1.generate_confirmation_token()
		confirmation = user2.confirm(token)
		self.assertFalse(confirmation)

	def test_confirm_good_token(self):
		user = db.session.query(User).\
			   filter(User.username == 'John Doe').first()
		token = user.generate_confirmation_token()
		confirmation = user.confirm(token)
		self.assertTrue(user.confirmed)