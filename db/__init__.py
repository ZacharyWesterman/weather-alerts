__all__ = ['users', 'alert_history', 'create_user']

from pymongo import MongoClient
import re
from datetime import datetime

client = MongoClient()
users = client.weather.users
alert_history = client.weather.alert_history

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
	client.weather.log.insert_one({
		'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
		'users': sent_list,
		'error': error,
	})
