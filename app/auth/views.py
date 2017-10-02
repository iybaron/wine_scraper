from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required
from . import auth
from .forms import LoginForm, RegistrationForm
from .. import db
from ..models import User

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
		flash('You have been registered. You can now login.')
		return redirect(url_for('auth.login'))

	# If handling a GET request, render the template 
	return render_template('auth/register.html', form=form)

# Called when users log out
@auth.route('/logout')
@login_required
def logout():
	# Log out user and return to front page
	logout_user()
	flash('You have been logged out.')
	return redirect(url_for('main.index'))