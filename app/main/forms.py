from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField

class SearchForm(FlaskForm):
	producer = StringField("Producer")
	year = SelectField(label='Year', choices=[tuple([i,i]) for i in range(2017, 1950, -1)], coerce=int)
	search = SubmitField("Search")