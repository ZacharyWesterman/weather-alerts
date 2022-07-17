import credentials
import users
import json
import datetime
from twilio.rest import Client

with open('last_sent.json', 'r') as fp:
	__CONFIG = json.load(fp)

def sent_today(name: str) -> dict:
	global __CONFIG

	if name not in __CONFIG:
		return False

	now = datetime.datetime.now()
	prev = datetime.datetime.strptime(__CONFIG[name], '%Y-%m-%d %H:%M:%S')

	return (prev + datetime.timedelta(days=1)).date() > now.date()

def send(name: str, message: str) -> None:
	global __CONFIG

	twilio = credentials.get('twilio')
	account_sid = twilio.get('account_sid')
	auth_token = twilio.get('auth_token')
	sender = twilio.get('phone')
	recipient = users.get(name).get('phone')

	sms_client = Client(account_sid, auth_token)

	result = sms_client.messages.create(body=message, from_=sender, to=recipient)

	#Log when we last sent each person a text
	__CONFIG[name] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	with open('last_sent.json', 'w') as fp:
		json.dump(__CONFIG, fp, indent=2)
