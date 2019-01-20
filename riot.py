# Standard modules

# Third-Party modules
import regex

# Project modules
import datastore

regional_endpoints = ['br1', 'eun1', 'euw1', 'jp1', 'kr',
                      'la1', 'la2', 'na1', 'oc1', 'tr1', 'ru', 'pbe1']


def get_base_url(region):
    return f'{region}.api.riotgames.com'


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


def get_headers():
    api_key = datastore.get_riot_api_key()

    return {'X-Riot-Token': api_key}
