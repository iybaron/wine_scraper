from flask import render_template, redirect, url_for, session
from flask_login import login_required
from .forms import SearchForm
from . import main
from ..scrape import scrape_all


# Front page
@main.route('/', methods=['GET'])
def index():
	return render_template('index.html')


# Handles user search input
@main.route('/search', methods=['GET', 'POST'])
@login_required
def search():
	scrape_all()
	producer = None 
	year = None
	form = SearchForm()

	# If handling a POST request, set values for the session and redirect
	if form.validate_on_submit():
		session['producer'] = form.producer.data
		session['year'] = form.year.data
		return redirect(url_for('.search'))

	# If handling a GET request, render the template 
	return render_template('search.html', form=form, producer=session.get('producer'), year=session.get('year'))
