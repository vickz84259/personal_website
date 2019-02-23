# Standard modules

# Third-Party modules
import requests
import regex

# Project modules

BASE_URL = 'https://api.lolesports.com/api/'


def get_tournaments(league_slug=None, league_id=None):
    endpoint = 'v1/leagues?'

    if league_slug is not None:
        endpoint = f'{endpoint}slug={league_slug}'
    elif league_id is not None:
        endpoint = f'{endpoint}id={league_id}'
    else:
        raise ValueError('No parameters given')

    url = f'{BASE_URL}{endpoint}'
    result = requests.get(url).json()

    return result['highlanderTournaments']


def get_vods():
    endpoint = 'v2/videos'
    url = f'{BASE_URL}{endpoint}'
    result = requests.get(url).json()

    return result['videos']


def get_youtube_id(youtube_url):
    re = regex.compile(r'''
        (?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu
        \.be\/)([^\"&?\/ ]{11})''', regex.VERBOSE)

    return re.search(youtube_url).group(1)


def get_tournament_id(reference):
    re = regex.compile(r'tournament:(\S+):game')
    return re.search(reference).group(1)
