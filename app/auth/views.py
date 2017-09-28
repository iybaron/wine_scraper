from flask import render_template
from . import auth

@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
	return render_template('auth/sign_up.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
	return render_template('auth/login.html')