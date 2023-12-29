import db
import datetime
import credentials
import skrunk_api

def sent_today(name: str) -> dict:
	user = db.users.find_one({'_id': name})
	if user.get('last_sent') is None:
		return False

	now = datetime.datetime.now()
	prev = datetime.datetime.strptime(user['last_sent'], '%Y-%m-%d %H:%M:%S')

	return (prev + datetime.timedelta(days=1)).date() > now.date()

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
