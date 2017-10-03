from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .forms import LoginForm, RegistrationForm
from .. import db
from ..models import User
from ..email import send_email

# Login page
@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	# If handling a POST request, verify user info and redirect
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user)
			return redirect(request.args.get('next') or url_for('main.index'))
		flash('Invalid username or password.')

	# If handling a GET request, render the template 
	return render_template('auth/login.html', form=form)

# Registration page
@auth.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	# If handling a POST request, validate user info, add new user and redirect
	if form.validate_on_submit():
		user = User(email=form.email.data, username=form.username.data, 
					password=form.password.data)
		db.session.add(user)
		db.session.commit()
		token = user.generate_confirmation_token()
		send_email(user.email, 'Confirm Your Account',
				   'auth/email/confirm', user=user, token=token)
		flash('A confirmation email has been sent to your inbox. \
			  Please confirm your account by clicking the link in that message.')
		return redirect(url_for('auth.login'))

	# If handling a GET request, render the template 
	return render_template('auth/register.html', form=form)

# Resends confirmation email
@auth.route('/confirm')
@login_required
def resend_confirmation():
	token = current_user.generate_confirmation_token()
	send_email(current_user.email, 'Confirm Your Account', 
			   'auth/email/confirm', user=current_user, 
			   token=token)
	flash('A new confirmation email has been sent to your inbox.')
	return redirect(url_for('main.index'))

# Handles confirmation of user emails
@auth.route('/confirm/<token>')
@login_required
def confirm(token):
	if current_user.confirmed:
		return redirect(url_for('main.index'))
	if current_user.confirm(token):
		flash('Your account has been confirmed.')
	else:
		flash('The confirmation link is invalid or has expired.')
	return redirect(url_for('main.index'))

# Called when users log out
@auth.route('/logout')
@login_required
def logout():
	# Log out user and return to front page
	logout_user()
	flash('You have been logged out.')
	return redirect(url_for('main.index'))

# Before request hook
@auth.before_app_request
def before_request():
	# If the user is not confirmed redirect to confirmation page
	if current_user.is_authenticated and not current_user.confirmed \
	and request.endpoint[:5] != 'auth.':
		return redirect(url_for('auth.unconfirmed'))

# Called when unconfirmed users make a request
@auth.route('/unconfirmed')
def unconfirmed():
	# If user is already confirmed, or not registered, redirect to front page
	if current_user.is_anonymous or current_user.confirmed:
		return redirect('main.index')
	return render_template('auth/unconfirmed.html', user=current_user)