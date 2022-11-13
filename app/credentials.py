import json

with open('config/credentials.json', 'r') as fp:
	__CONFIG = json.load(fp)

def get(key: str) -> dict:
	global __CONFIG
	return __CONFIG.get(key)
