from flask import render_template, redirect, url_for, session
from flask_login import login_required
from .forms import SearchForm
from . import main

@main.route('/', methods=['GET'])
def index():
	return render_template('index.html')

@main.route('/search', methods=['GET', 'POST'])
@login_required
def search():
	producer = None 
	year = None
	form = SearchForm()
	if form.validate_on_submit():
		session['producer'] = form.producer.data
		session['year'] = form.year.data
		return redirect(url_for('.search'))
	return render_template('search.html', form=form, producer=session.get('producer'), year=session.get('year'))
