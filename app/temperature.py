from . import users
from . import settings
from datetime import date
import time

def below_user_min(name: str, forecast: dict) -> list:
	user = users.get(name)
	if user.get('min') is not None:
		if user['min'] == False:
			return []
		min_temp = user['min']
	else:
		min_temp = settings.get('min_temp')

	return [
		str(date.fromtimestamp(day['dt'])) for day in forecast['daily'] if day['temp']['min'] <= min_temp and day['dt'] > time.time()
	]

def above_user_max(name: str, forecast: dict) -> list:
	user = users.get(name)
	if user.get('max') is not None:
		if user['max'] == False:
			return []
		max_temp = user['max']
	else:
		max_temp = settings.get('max_temp')

	return [
		str(date.fromtimestamp(day['dt'])) for day in forecast['daily'] if day['temp']['max'] >= max_temp and day['dt'] > time.time()
	]

def user_min(name: str) -> float:
	user = users.get(name)
	if user == None:
		return None

	val = user.get('min')
	if val is None:
		val = settings.get('min_temp')
	return val

def user_max(name: str) -> float:
	user = users.get(name)
	if user == None:
		return None

	val = user.get('max')
	if val is None:
		val = settings.get('max_temp')
	return val
