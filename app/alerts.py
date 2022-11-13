from . import credentials
from . import users
import db
import datetime
from twilio.rest import Client

def sent_today(name: str) -> dict:
	user = db.users.find_one({'_id': name})
	if user.get('last_sent') is None:
		return False

	now = datetime.datetime.now()
	prev = datetime.datetime.strptime(user['last_sent'], '%Y-%m-%d %H:%M:%S')

	return (prev + datetime.timedelta(days=1)).date() > now.date()

def send(name: str, message: str, *, log = True) -> None:
	twilio = credentials.get('twilio')
	account_sid = twilio.get('account_sid')
	auth_token = twilio.get('auth_token')
	sender = twilio.get('phone')
	recipient = users.get(name).get('phone')

	sms_client = Client(account_sid, auth_token)

	result = sms_client.messages.create(body=message, from_=sender, to=recipient)

	if log:
		#Log when we last sent each person a text
		now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		db.users.update_one(
			{'_id': name},
			{'$set': {'last_sent': now}}
		)
		db.alert_history.insert_one({
			'to': name,
			'message': message,
		})
