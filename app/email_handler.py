from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail


# Run in background thread to prevent blocking
def send_async_email(app, msg):
	with app.app_context():
		mail.send(msg)


def send_email(to, subject, template, **kwargs):
	app = current_app._get_current_object()
	# Construct email message
	msg = Message(app.config['SCRAPER_MAIL_SUBJECT_PREFIX'] + subject, 
					sender=app.config['SCRAPER_MAIL_SENDER'], recipients=[to])
	msg.body = render_template(template + '.txt', **kwargs)
	msg.html = render_template(template + '.html', **kwargs)
	
	# Create thread for asynchronous email handling
	thr = Thread(target=send_async_email, args=[app, msg])
	thr.start()
	return thr