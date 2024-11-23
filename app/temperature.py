from . import users
from . import settings
from datetime import date
import time

def below_user_min(name: str, forecast: dict) -> list:
	user = users.get(name)
	if user.get('min') is not None:
		if user['min'].get('disable'):
			return []
		elif user['min'].get('default'):
			min_temp = settings.get('min_temp')
		else:
			min_temp = user['min'].get('value')
	else:
		min_temp = settings.get('min_temp')

	return [
		str(date.fromtimestamp(day['dt'])) for day in forecast['daily'] if day['temp']['min'] <= min_temp and day['dt'] > time.time()
	]

def above_user_max(name: str, forecast: dict) -> list:
	user = users.get(name)
	if user.get('max') is not None:
		if user['max'].get('disable'):
			return []
		elif user['max'].get('default'):
			max_temp = settings.get('max_temp')
		else:
			max_temp = user['max'].get('value')
	else:
		max_temp = settings.get('max_temp')

	return [
		str(date.fromtimestamp(day['dt'])) for day in forecast['daily'] if day['temp']['max'] >= max_temp and day['dt'] > time.time()
	]

def user_min(name: str) -> float:
	user = users.get(name)
	if user == None:
		return None
	
	if user.get('min') is not None:
		if user['min'].get('disable'):
			return None
		elif user['min'].get('default'):
			return settings.get('min_temp')

		return user['min'].get('value')

	return settings.get('min_temp')

def user_max(name: str) -> float:
	user = users.get(name)
	if user == None:
		return None

	if user.get('max') is not None:
		if user['max'].get('disable'):
			return None
		elif user['max'].get('default'):
			return settings.get('max_temp')

		return user['max'].get('value')

	return settings.get('max_temp')