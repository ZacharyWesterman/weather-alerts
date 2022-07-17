import settings
import credentials
import requests
import json

__CACHE = {}

class WeatherAPIFailure(Exception):
	def __init__(self, status_code):
		self.code = status_code

	def __str__(self):
		return f'Unable to fetch weather data. Status code {self.code}'

def fetch(*, lat: float, lon: float) -> dict:
	global __CACHE

	#If weather data has already been fetched for these coords,
	#just return the cached value.
	if lat in __CACHE and lon in __CACHE[lat]:
		return __CACHE[lat][lon]

	weather = settings.get('openweathermap')
	cred = credentials.get('openweathermap')

	api_url = weather.get('api_url')
	exclude = weather.get('exclude')
	units = weather.get('units')
	app_id = cred.get('appid')

	url = f'{api_url}?lat={lat}&lon={lon}&exclude={exclude}&units={units}&appid={app_id}'
	result = requests.get(url)

	if result.status_code != 200:
		raise WeatherAPIFailure(result.status_code)

	if lat not in __CACHE:
		__CACHE[lat] = {}
	__CACHE[lat][lon] = json.loads(result.text)

	return __CACHE[lat][lon]
