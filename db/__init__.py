__all__ = ['log']

import skrunk_api
from app import credentials

def log(sent_list: list, error: str|None, *, debug: bool = False) -> None:
	cred = credentials.get('skrunk_api')
	api = skrunk_api.Session(cred.get('api_key', ''), cred.get('url', ''))

	if debug:
		pass
	else:
		api.log_weather_alert(users = sent_list, error = error)
