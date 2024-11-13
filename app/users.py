import skrunk_api
from . import credentials
from functools import cache

__users = {}

@cache
def all() -> list:
	cred = credentials.get('skrunk_api')
	api = skrunk_api.Session(cred.get('api_key'), cred.get('url'))
	users = [i for i in api.call('getWeatherUsers') if not i.get('exclude')]

	#Add to user cache
	for i in users:
		__users[i['username']] = i

	return [(data['username'], data) for data in users]

@cache
def get(name: str) -> dict:
	if name in __users:
		return __users[name]

	cred = credentials.get('skrunk_api')
	api = skrunk_api.Session(cred.get('api_key'), cred.get('url'))
	user_data = api.call('getWeatherUser', {'username': name})

	__users[user_data['username']] = user_data
	return user_data
