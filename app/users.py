import db

def all() -> list:
	return [(data['_id'], data) for data in db.users.find({'exclude': False})]

def get(name: str) -> dict:
	return db.users.find_one({'_id': name})
