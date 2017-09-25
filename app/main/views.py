from flask import Flask, render_template, url_for
from forms import SearchForm
from . import main_blueprint

@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
	return render_template('sign_up.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	return render_template('login.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
	producer = None 
	year = None
	form = SearchForm()
	if form.validate_on_submit():
		session['producer'] = form.producer.data
		session['year'] = form.year.data
		return redirect(url_for('search'))
	return render_template('form_bs.html', form=form, producer=session.get('producer'), year=session.get('year'))
