import json

with open('people.json', 'r') as fp:
	__CONFIG = json.load(fp)

def all() -> list:
	global __CONFIG
	return [(name, __CONFIG[name]) for name in __CONFIG if not __CONFIG[name].get('exclude')]

def get(name: str) -> dict:
	global __CONFIG
	return __CONFIG.get(name)
