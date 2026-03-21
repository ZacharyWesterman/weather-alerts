from . import users
from . import settings
from datetime import date
import time


def get_setting(username: str, min_max: str) -> float | None:
    user = users.get(username)
    if user.get(min_max) is not None:
        if user[min_max].get('disable'):
            return None
        elif user[min_max].get('default'):
            return settings.get(f'{min_max}_temp')
        return user[min_max].get('value')
    return settings.get(f'{min_max}_temp')


def future_days(forecast: dict) -> list[dict]:
    return [
        day for day in forecast['daily'] if day['dt'] > time.time()
    ]


def format_days(daylist: list[dict]) -> list[str]:
    return [
        str(date.fromtimestamp(day['dt'])) for day in daylist
    ]


def above_user_min(name: str, forecast: dict) -> list:
    min_temp = get_setting(name, 'min')
    if min_temp is None:
        return []
    return format_days([day for day in future_days(forecast) if day['temp']['min'] > min_temp])


def below_user_min(name: str, forecast: dict) -> list:
    min_temp = get_setting(name, 'min')
    if min_temp is None:
        return []
    return format_days([day for day in future_days(forecast) if day['temp']['min'] <= min_temp])


def above_user_max(name: str, forecast: dict) -> list:
    max_temp = get_setting(name, 'max')
    if max_temp is None:
        return []
    return format_days([day for day in future_days(forecast) if day['temp']['max'] >= max_temp])


def below_user_max(name: str, forecast: dict) -> list:
    max_temp = get_setting(name, 'max')
    if max_temp is None:
        return []
    return format_days([day for day in future_days(forecast) if day['temp']['max'] < max_temp])


def user_min(name: str) -> float | None:
    user = users.get(name)
    if user == None:
        return None

    if user.get('min') is not None:
        if user['min'].get('disable'):
            return None
        elif user['min'].get('default'):
            return settings.get('min_temp')

        return user['min'].get('value')

    return settings.get('min_temp')


def user_max(name: str) -> float | None:
    user = users.get(name)
    if user == None:
        return None

    if user.get('max') is not None:
        if user['max'].get('disable'):
            return None
        elif user['max'].get('default'):
            return settings.get('max_temp')

        return user['max'].get('value')

    return settings.get('max_temp')
