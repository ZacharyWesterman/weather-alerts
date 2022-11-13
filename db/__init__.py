__all__ = ['users', 'alert_history', 'create_user']

from pymongo import MongoClient
import re

client = MongoClient('mongodb://192.168.1.184:27017')
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
