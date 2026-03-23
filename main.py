#!/usr/bin/env python3

from sys import argv
from app import users, weather, temperature, alerts
from db import log

if __name__ == '__main__':
    log_sent_list = []

    try:
        sent_list = []
        ADMIN = 'zachary'
        DRY_RUN = '--dry-run' in argv
        DEBUG = '--debug' in argv

        for name, user in users.all():

            if alerts.sent_today(name):
                if DRY_RUN:
                    print(f'Already sent alert to {name}, skipping.')
                continue

            forecast = weather.fetch(lat=user.get('lat'), lon=user.get('lon'))
            # number of future days (excluding today)
            forecast_num_days = len(forecast['daily']) - 1
            below = temperature.below_user_min(name, forecast)
            above = temperature.above_user_max(name, forecast)

            if len(below) or len(above):
                min = temperature.user_min(name)
                max = temperature.user_max(name)

                title = 'ZW Automated Weather Warning'
                msg = ''

                daytext = 'all week' if forecast_num_days == 7 else f'for {forecast_num_days} day{"s" if forecast_num_days != 1 else ""}'

                plural = '' if len(below) == 1 else 's'
                if len(below) == forecast_num_days:
                    msg += f'Low{plural} at or below {min}F {daytext}.'
                elif len(below) / forecast_num_days >= 0.7:
                    msg += f'Low{plural} at or below {min}F {daytext}, EXCEPT FOR:\n' \
                        '\n'.join(temperature.above_user_min(name, forecast))
                elif len(below):
                    msg += f'Low{plural} at or below {min}F on:\n' + \
                        '\n'.join(below)

                plural = '' if len(above) == 1 else 's'
                if len(above) == forecast_num_days:
                    msg += f'High{plural} at or above {max}F {daytext}.'
                elif len(above) / forecast_num_days >= 0.7:
                    print(above)
                    msg += f'High{plural} at or above {max}F {daytext}, EXCEPT FOR:\n' + \
                        '\n'.join(temperature.below_user_max(name, forecast))
                elif len(above):
                    msg += f'High{plural} at or above {max}F on:\n' + \
                        '\n'.join(above)
                msg += '\nChecking local forecasts is recommended.'

                if not DRY_RUN:
                    alerts.send(name, title, msg, debug=DEBUG)
                    if name != ADMIN:
                        sent_list += [name]
                    log_sent_list += [name]
                else:
                    print(name)
                    print(msg)

        if len(sent_list) and not DRY_RUN:
            msg = 'Sent alerts to ' + ', '.join(sent_list)
            alerts.notify(ADMIN, 'Weather Alert Log:', msg, debug=DEBUG)

        # Always log that this pgm ran successfully
        log(log_sent_list, None, debug=DEBUG)

    except Exception as e:
        log(log_sent_list, str(e), debug=DEBUG)
        raise e
