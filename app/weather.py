from . import settings
from . import credentials
import requests
import json
from functools import cache

class WeatherAPIFailure(Exception):
	def __init__(self, status_code):
		self.code = status_code

	def __str__(self):
		return f'Unable to fetch weather data. Status code {self.code}'

@cache
def fetch(*, lat: float, lon: float) -> dict:
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

	return json.loads(result.text)
