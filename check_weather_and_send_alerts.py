#!/usr/bin/env python3

import requests, json, time
import datetime
from twilio.rest import Client

with open('settings.json', 'r') as fp: SETTINGS = json.load(fp)
with open('credentials.json', 'r') as fp: CREDENTIALS = json.load(fp)
with open('people.json', 'r') as fp: PEOPLE = json.load(fp)
try:
	with open('last_sent.json', 'r') as fp: LAST_SENT = json.load(fp)
except:
	LAST_SENT = {}

def alert_message(days):
	global SETTINGS
	min_temp = SETTINGS['openweathermap']['min_temp']
	plural = 's' if len(days) > 1 else ''
	msg = f'ZW Automated Weather Warning: Low{plural} below {min_temp}F on the following date{plural}:'
	for day in days: msg += f'\n{day}'
	msg += '\nChecking local forecasts is recommended.'
	return msg

def get_weather(lat, lon):
	global CREDENTIALS, SETTINGS

	api_url = SETTINGS['openweathermap']['api_url']
	exclude = SETTINGS['openweathermap']['exclude']
	units = SETTINGS['openweathermap']['units']
	appid = CREDENTIALS['openweathermap']['appid']

	result = requests.get(f'{api_url}?lat={lat}&lon={lon}&exclude={exclude}&units={units}&appid={appid}')
	if result.status_code != 200: raise Exception(f'Unable to fetch weather data. Status code {result.status_code}')

	return json.loads(result.text)

def get_temps_below_min(weather):
	global SETTINGS
	return [ datetime.date.fromtimestamp(i['dt']) for i in weather['daily'] if (i['temp']['min'] <= SETTINGS['openweathermap']['min_temp']) and (i['dt'] > time.time()) ]

#Loop through all people to check for low temps in their area
for name in PEOPLE:
	person = PEOPLE[name]
	if 'exclude' in person and person['exclude']: continue

	current_date = datetime.datetime.now()
	if name in LAST_SENT:
		prev = datetime.datetime.strptime(LAST_SENT[name], '%Y-%m-%d %H:%M:%S')
		# print(prev + datetime.timedelta(hours=23), current_date)
		if (prev + datetime.timedelta(hours=23)) >= current_date:
			continue #Don't send another text to this person if they've already been alerted today.

	#Get the weather for the current recipient's latitude/longitude
	weather = get_weather(person['lat'], person['lon'])
	low_list = get_temps_below_min(weather)

	#If there are days in the forecast that are below the min,
	#Create and send a "warning" text message to the recipient
	if len(low_list):
		account_sid = CREDENTIALS['twilio']['account_sid']
		auth_token = CREDENTIALS['twilio']['auth_token']
		sms_client = Client(account_sid, auth_token)

		sender = CREDENTIALS['twilio']['phone']
		recipient = person['phone']
		msg = alert_message(low_list)

		result = sms_client.messages.create(body = msg, from_ = sender, to = recipient)

		#log when we last sent each person a text
		LAST_SENT[name] = current_date.strftime('%Y-%m-%d %H:%M:%S')

#log when we last sent each person a text
with open('last_sent.json', 'w') as fp:
	json.dump(LAST_SENT, fp, indent=2)
