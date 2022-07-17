#!/usr/bin/env python3

import users
import weather
import temperature
import alerts

if __name__ == '__main__':
	for name, user in users.all():

		if alerts.sent_today(name):
			continue

		forecast = weather.fetch(lat=user.get('lat'), lon=user.get('lon'))
		below = temperature.below_user_min(name, forecast)
		above = temperature.above_user_max(name, forecast)

		if len(below) or len(above):
			min = temperature.user_min(name)
			max = temperature.user_max(name)

			msg = 'ZW Automated Weather Warning:'
			if len(below):
				plural = '' if len(below) == 1 else 's'
				msg += f'\nLow{plural} at or below {min}F on:\n' + '\n'.join(below)
			if len(above):
				plural = '' if len(above) == 1 else 's'
				msg += f'\nHigh{plural} at or above {max}F on:\n' + '\n'.join(above)
			msg += '\nChecking local forecasts is recommended.'

			alerts.send(name, msg)
