import datetime
import skrunk_api
from . import credentials, users

def sent_today(name: str) -> dict:
	user = users.get(name)
	if user.get('last_sent') is None:
		return False

	now = datetime.datetime.now()
	prev = datetime.datetime.strptime(user['last_sent'], '%a, %d %b %Y %H:%M:%S %Z')

	return (prev + datetime.timedelta(days=1)).date() > now.date()

def notify(name: str, title: str, message: str) -> None:
	cred = credentials.get('skrunk_api')
	api = skrunk_api.Session(cred.get('api_key'), cred.get('url'))

	try:
		api.call('sendNotification', {
			'username': name,
			'title': title,
			'body': message,
			'category': 'admin-alert',
		})
	except skrunk_api.SessionError as e:
		#Should only really fail if connection to the server fails
		print(e)

def send(name: str, title: str, message: str, *, log = True) -> None:
	cred = credentials.get('skrunk_api')
	api = skrunk_api.Session(cred.get('api_key'), cred.get('url'))

	try:
		api.call('sendNotification', {
			'username': name,
			'title': title,
			'body': message,
			'category': 'weather',
		})
	except skrunk_api.SessionError as e:
		#Should only really fail if connection to the server fails
		print(e)

	#Log when we last sent each person a text
	api.call('logUserWeatherAlert', {
		'username': name,
		'message': message,
	})
