__all__ = ['log', 'create_user']

import re
import skrunk_api
from app import credentials

def create_user(*, id: str, lat: float, lon: float, phone: str, exclude: bool = False) -> None:
	phone = re.sub('[^0-9]', '', phone)
	if len(phone) < 11:
		raise Exception(f'ERROR: Invalid phone number "+{phone}"')

	cfg = {
		'_id': id,
		'lat': lat,
		'lon': lon,
		'phone': f'+{phone}',
		'exclude': exclude,
	}

def log(sent_list: list, error: str) -> None:
	cred = credentials.get('skrunk_api')
	api = skrunk_api.Session(cred.get('api_key'), cred.get('url'))

	api.call('logWeatherAlert', {
		'users': sent_list,
		'error': error,
	})
