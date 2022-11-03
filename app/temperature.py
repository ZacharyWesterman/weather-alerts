import .users
import .settings
from datetime import date
import time

def below_user_min(name: str, forecast: dict) -> list:
	user = users.get(name)
	if 'min' in user:
		if user['min'] == None:
			return []
		min_temp = user['min']
	else:
		min_temp = settings.get('min_temp')

	now = time.time()
	return [
		str(date.fromtimestamp(day['dt'])) for day in forecast['daily'] if day['temp']['min'] <= min_temp and day['dt'] > time.time()
	]

def above_user_max(name: str, forecast: dict) -> list:
	user = users.get(name)
	if 'max' in user:
		if user['max'] == None:
			return []
		max_temp = user['max']
	else:
		max_temp = settings.get('max_temp')

	now = time.time()
	return [
		str(date.fromtimestamp(day['dt'])) for day in forecast['daily'] if day['temp']['max'] >= max_temp and day['dt'] > time.time()
	]

def user_min(name: str) -> float:
	user = users.get(name)
	if user == None:
		return None

	return user['min'] if 'min' in user else settings.get('min_temp')

def user_max(name: str) -> float:
	user = users.get(name)
	if user == None:
		return None

	return user['max'] if 'max' in user else settings.get('max_temp')
