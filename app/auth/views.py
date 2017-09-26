from flask import render_template
from . import auth

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
	return render_template('sign_up.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	return render_template('login.html')