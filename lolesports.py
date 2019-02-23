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


def validate(youtube_url, reference):
    result = True
    try:
        get_youtube_id(youtube_url)
        get_tournament_id(reference)
    except (TypeError, AttributeError):
        result = False

    return result


def vods():
    for vod in get_vods():
        youtube_url = vod['source']
        reference = vod['reference']
        if not validate(youtube_url, reference):
            continue

        yield vod


def get_mapping(tournament, game_id):
    mapping = {}

    try:
        for bracket in tournament['brackets'].values():
            for match in bracket['matches'].values():
                state = match.get('state', 'unresolved')
                if state == 'resolved':
                    for game in match['games'].values():
                        if game['id'] == game_id:

                            platform_id = game.get('platformId')
                            if platform_id is not None:
                                mapping['game_id'] = game_id
                                mapping['platform_id'] = platform_id

                                mapping['match_id'] = match['id']
                                mapping['tournament_id'] = tournament['id']

                            raise StopIteration
    except StopIteration:
        pass

    return mapping
