#!/usr/bin/env python3

from sys import argv
from app import users, weather, temperature, alerts
from db import log

if __name__ == '__main__':
	log_sent_list = []

	try:
		sent_list = []
		ADMIN = 'zachary'
		DRY_RUN = True if '--dry-run' in argv else False

		for name, user in users.all():

			if alerts.sent_today(name):
				if DRY_RUN:
					print(f'Already sent alert to {name}, skipping.')
				continue

			forecast = weather.fetch(lat=user.get('lat'), lon=user.get('lon'))
			below = temperature.below_user_min(name, forecast)
			above = temperature.above_user_max(name, forecast)

			if len(below) or len(above):
				min = temperature.user_min(name)
				max = temperature.user_max(name)

				title = 'ZW Automated Weather Warning'
				msg = ''
				if len(below):
					plural = '' if len(below) == 1 else 's'
					msg += f'\nLow{plural} at or below {min}F on:\n' + '\n'.join(below)
				if len(above):
					plural = '' if len(above) == 1 else 's'
					msg += f'\nHigh{plural} at or above {max}F on:\n' + '\n'.join(above)
				msg += '\nChecking local forecasts is recommended.'

				if not DRY_RUN:
					alerts.send(name, title, msg)
					if name != ADMIN:
						sent_list += [name]
					log_sent_list += [name]
				else:
					print(name)
					print(msg)

		if len(sent_list) and not DRY_RUN:
			msg = 'Sent alerts to ' + ', '.join(sent_list)
			alerts.send(ADMIN, 'Weather Alert Log:', msg, log = False)

		# Always log that this pgm ran successfully
		log(log_sent_list, None)

	except Exception as e:
		log(log_sent_list, str(e))
		raise e
