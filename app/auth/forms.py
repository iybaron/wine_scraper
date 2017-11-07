from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import Required, Email, Length, Regexp, EqualTo
from ..models import User

# Form for login page
class LoginForm(FlaskForm):
	email = StringField('Email', validators=[Required(), Length(1, 64), 
											 Email()])
	password = PasswordField('Password', validators=[(Required())])
	submit = SubmitField('Log In')


# Form for registration page
class RegistrationForm(FlaskForm):
	# Email is required and must be in the proper format
	email = StringField('Email', validators=[Required(), Length(1, 64),
											 Email()])
	
	# Username is required, must start with a letter, and may only contain 
	# letters, numbers, dots, and underscores
	username = StringField("Username", validators=[
		Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 
										  'Usernames must have only letters, '
										  'numbers, dots and underscores')])
	
	# password is required and must match password2
	password = PasswordField('Password', validators=[
		Required(), EqualTo('password2', message='Passwords must match.')])
	# password2 must match password
	password2 = PasswordField('Confirm Password', validators=[Required()])
	
	submit = SubmitField('Sign Up')

	# Custom validation for email
	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('Email already registered.')

	# Custom validation for username
	def validate_username(self, field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError('Username already in use.')
			