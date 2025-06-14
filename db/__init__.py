__all__ = ['log']

import re
import skrunk_api
from app import credentials

def log(sent_list: list, error: str) -> None:
	cred = credentials.get('skrunk_api')
	api = skrunk_api.Session(cred.get('api_key'), cred.get('url'))

	api.call('logWeatherAlert', {
		'users': sent_list,
		'error': error,
	})
