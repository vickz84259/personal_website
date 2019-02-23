# Standard modules
import ast

# Third-Party modules
import requests
import regex

# Project modules
import datastore

BASE_URL = 'https://api.lolesports.com/api/'


class InvalidIdException(Exception):
    """Raised when the youtube id given cannot be found"""


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


def get_vod(youtube_id):
    result = {}
    for vod in vods():
        if get_youtube_id(vod['source']) == youtube_id:
            result = vod
            break

    return result


def get_tournament(league_id, tournament_id):
    for tournament in get_tournaments(league_id=league_id):
        if tournament['id'] == tournament_id:
            return tournament


def get_match_details(youtube_id):
    redis_db = datastore.get_redis_connection()
    match_details = redis_db.get(youtube_id)

    if match_details is None:
        vod = get_vod(youtube_id)
        if not vod:
            raise InvalidIdException

        tournament_id = get_tournament_id(vod['reference'])
        league_id = redis_db.get(tournament_id)
        tournament = get_tournament(league_id, tournament_id)

        mapping = get_mapping(tournament, vod['game'])
        if mapping:
            redis_db.set(youtube_id, str(mapping))

        result = mapping
    else:
        result = ast.literal_eval(match_details)

    return result
