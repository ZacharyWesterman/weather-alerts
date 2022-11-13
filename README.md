# weather-alerts
Send automated text alerts about local freezing forecasts.

## Dependencies
Run `./setup.sh` to set up the virtual environment and install dependencies.

## Before getting started

You will need a [twilio](https://www.twilio.com/) account with at least 1 phone number to send messages from (**Note: this costs money!**).
You will also need an [openweathermap](https://openweathermap.org/) api key. The free option should be more than enough, but do note that the weather will be checked once for every unique latitude/longitude in `person.json`.

## Initial setup

To get the main script to work, a few configuration files need to be created in the `data/` directory of this project: `credentials.json` and `people.json`.
These files will contain sensitive data so **DO NOT COMMIT THEM!**
Below are some example layouts.

### config/credentials.json
```json
{
	"openweathermap": {
		"appid": "your_app_id_here"
	},

	"twilio": {
		"account_sid": "your_account_sid_here",
		"auth_token": "your_auth_token_here",
		"phone": "+ABBBCCCDDDD"
	}
}
```
Make sure you input the phone number as `+ABBBCCCDDDD`, not `+A (BBB) CCC-DDDD` or `(BBB) CCC-DDDD`.
Basically, include the plus, country code and extension, but not any spaces or punctuation. Do **NOT** commit this file!

### data/people.json
```json
{
	"person_1": {
		"lat": 12.34,
		"lon": 12.34,
		"phone": "+ABBBCCCDDDD"
	},
	"person_2": {
		"lat": 12.34,
		"lon": 12.34,
		"phone": "+ABBBCCCDDDD",
		"max": 100,
		"min": null,
		"exclude": true
	}
}
```
Note that the `exclude`, `min` and `max` attributes are optional, as they have default values.

* `exclude` (true/false, default is false): If true, do not send alerts to this person.
* `min` (number or null, default is 34.0): Send temp alerts if temp is at or below this. If null, do not send alerts about low temps.
* `max` (number or null, default is 110.0): Send temp alerts if temp is at or above this. If null, do not send alerts about high temps.

## Running the program
You can run this program manually by running `./run.sh`, but ideally this would be set to automatically run every now and then.
Something like the following cron job would work fine:
```
0 6-22 * * * /path/to/weather-alerts/run.sh
```
