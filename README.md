# weather-alerts
Send automated text alerts about local freezing forecasts.

## Dependencies
```
pip3 install twilio
```
## Before getting started

You will need a [twilio](https://www.twilio.com/) account with at least 1 phone number to send messages from (**Note: this costs money!**).
You will also need an [openweathermap](https://openweathermap.org/) api key. The free option should be more than enough, but do note that the weather will be checked exactly once for each item in `person.json`.

## Initial setup

To get the main script to work, a few configuration files need to be created in the root directory of this project: `credentials.json` and `people.json`.
These files will contain sensitive data so **DO NOT COMMIT THEM!**
Below are some example

### credentials.json
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
Basically, include the plus, country code and extension, but not any spaces or punctuation.

### people.json
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
		"exclude": true
	}
}
```
Note that the `exclude` attribute is optional, but if it is set to true, then that item will be ignored (exactly as if it was not in the config at all).
