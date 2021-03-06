# Standard modules

# Third-Party modules
import regex
import requests

# Project modules
import datastore

regional_endpoints = ['br1', 'eun1', 'euw1', 'jp1', 'kr',
                      'la1', 'la2', 'na1', 'oc1', 'tr1', 'ru', 'pbe1']

APP_RL_TYPE = 'X-App-Rate-Limit'
METHOD_RL_TYPE = 'X-Method-Rate-Limit'


class ErrorResponse:

    def __init__(self, status_code, headers):
        self.status_code = status_code
        self.headers = headers


def is_valid_region(region):
    result = True
    if region not in regional_endpoints:
        result = False

    return result


def is_valid_summoner(summoner_name):
    result = True
    if not regex.match('^[0-9\\p{L} _\\.]{3,16}$', summoner_name):
        result = False

    return result


def get_method(endpoint):
    str_list = endpoint.split('/')[:-1]
    return '/'.join(str_list)


def __check_rate_limit(type_name):
    result = True

    redis_db = datastore.get_redis_connection()
    limits = redis_db.get(type_name)

    if limits is not None:
        for time, calls in __get_limits(limits).items():
            calls_made = redis_db.get(f'{type_name}:{time}')

            if calls_made is not None and int(calls_made) >= calls:
                result = False

    return result


def assert_rate_limit(region, endpoint):
    result = False

    app_type_name = f'{APP_RL_TYPE}:{region}'

    method = get_method(endpoint)
    method_type_name = f'{METHOD_RL_TYPE}:{region}:{method}'

    if (__check_rate_limit(app_type_name) and
            __check_rate_limit(method_type_name)):
        result = True

    return result


def __get_limits(limits):
    limits_list = limits.split(',')

    result = {}
    for limit in limits_list:
        rate_limit = limit.split(':')
        time = rate_limit[1]
        calls = rate_limit[0]

        result[time] = int(calls)

    return result


def __set_rate_limit(type, limits, limit_counts, region, endpoint=None):
    redis_db = datastore.get_redis_connection()

    if type == APP_RL_TYPE:
        type_name = f'{APP_RL_TYPE}:{region}'
    elif type == METHOD_RL_TYPE:
        method = get_method(endpoint)
        type_name = f'{METHOD_RL_TYPE}:{region}:{method}'

    rate_limit = redis_db.get(type_name)
    if rate_limit is None or rate_limit != limits:
        redis_db.set(type_name, limits)

    for time, calls_made in __get_limits(limit_counts).items():
        redis_db.set(
            f'{type_name}:{time}',
            calls_made,
            ex=int(time))


def set_rate_limit(region, endpoint, headers):
    __set_rate_limit(
        APP_RL_TYPE,
        headers['X-App-Rate-Limit'],
        headers['X-App-Rate-Limit-Count'],
        region)

    __set_rate_limit(
        METHOD_RL_TYPE,
        headers['X-Method-Rate-Limit'],
        headers['X-Method-Rate-Limit-Count'],
        region,
        endpoint)


def get(region, endpoint):
    if assert_rate_limit(region, endpoint):
        api_key = datastore.get_riot_api_key()
        headers = {'X-Riot-Token': api_key}

        url = f'https://{region}.api.riotgames.com{endpoint}'
        result = requests.get(url, headers=headers)

        set_rate_limit(region, endpoint, result.headers)
    else:
        result = ErrorResponse(429, {'Retry-After': 10})

    return result
