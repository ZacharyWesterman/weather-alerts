# weather-alerts
Send automated notifications about local freezing forecasts.

Note: this repo is meant to work as a runner for [ZacharyWesterman/skrunk]. As such, it interacts with the API of said server, and cannot be used without it.

## Dependencies
Run `./setup.sh` to set up the virtual environment and install dependencies.

## Before getting started

You will need an [openweathermap](https://openweathermap.org/) api key. The free option should be more than enough, but do note that the weather will be checked once for every unique latitude/longitude in the weather.users DB collection.
You will also need an API key for [ZacharyWesterman/skrunk]. See the repo for how to set that up.

## Initial setup

To get the main script to work, a configuration file needs to be created: `config/credentials.json`.
This file will contain sensitive data so **DO NOT COMMIT IT!**
Below is an example layout:

### config/credentials.json
```json
{
	"openweathermap": {
		"appid": "your_app_id_here"
	},

	"skrunk_api": {
		"api_key": "your_api_key_here",
		"url": "https://example.com"
	}
}
```

## Running the program
You can run this program manually by running `./run.sh`, but ideally this would be set to automatically run every now and then.
Something like the following cron job would work fine:
```
0 6-22 * * * /path/to/weather-alerts/run.sh
```

When this program runs, it will search for all weather.users with the `exclude` field set to `false`, check openweathermap with their latitude and longitude, and if the forecasted temperature is greater than their max or lower than their min, calls out to the Skrunk API to send the user an alert.
