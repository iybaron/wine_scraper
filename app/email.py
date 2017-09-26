import os
from threading import Thread
from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)
mail = Mail(app)

def send_async_email(app, msg):
	with app.app_context():
		mail.send(msg)

def send_email(to, subject, template, **kwargs):
	msg = Message(app.config['SCRAPER_MAIL_SUBJECT_PREFIX'] + subject, 
					sender=app.config['SCRAPER_MAIL_SENDER'], recipients=[to])
	msg.body = render_template(template + '.txt', **kwargs)
	thr = Thread(target=send_async_email, args=[app, msg])
	thr.start()
	return thr