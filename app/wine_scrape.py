import os
from flask import Flask, render_template, redirect, url_for, session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
bootstrap = Bootstrap(app)

class SearchForm(FlaskForm):
	producer = StringField("Producer")
	year = SelectField(label='Year', choices=[tuple([i,i]) for i in range(2017, 1950, -1)], coerce=int)
	search = SubmitField("Search")

@app.route('/', methods=['GET', 'POST'])
def index():
	producer = None 
	year = None
	form = SearchForm()
	if form.validate_on_submit():
		session['producer'] = form.producer.data
		session['year'] = form.year.data
		return redirect(url_for('index'))
	return render_template('form_bs.html', form=form, producer=session.get('producer'), year=session.get('year'))

if __name__ == "__main__":
	app.run()