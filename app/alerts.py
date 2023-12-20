from . import credentials
from . import users
import db
import datetime

#Import server interaction
#This directly interacts with https://github.com/ZacharyWesterman/server!
#Be it via a symlink, submodule, whatever.
from application.db import init_db, notification

init_db()

def sent_today(name: str) -> dict:
	user = db.users.find_one({'_id': name})
	if user.get('last_sent') is None:
		return False

	now = datetime.datetime.now()
	prev = datetime.datetime.strptime(user['last_sent'], '%Y-%m-%d %H:%M:%S')

	return (prev + datetime.timedelta(days=1)).date() > now.date()

def send(name: str, title: str, message: str, *, log = True) -> None:
	notification.send(title, message, name, category = 'weather')

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
