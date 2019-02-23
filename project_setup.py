# Standard modules

# Third-Party modules
import requests

# Project modules
import datastore
import lolesports


def get_leagues():
    x_api_key = datastore.get_relapi_key()
    headers = {'x-api-key': x_api_key}

    base_url = 'https://prod-relapi.ewp.gg/persisted/gw'
    url = f'{base_url}/getLeagues?hl=en-GB'
    result = requests.get(url, headers=headers).json()

    return result['data']['leagues']


def _setup(return_tournaments=True):
    tournament_map = {}
    league_map = {}

    leagues = get_leagues()
    for league in leagues:
        tournaments = lolesports.get_tournaments(league['slug'])

        for tournament in tournaments:
            tournament_id = tournament['id']
            league_map[tournament_id] = tournament['leagueId']

            if return_tournaments:
                tournament_map[tournament_id] = tournament

    redis_db = datastore.get_redis_connection()
    redis_db.mset(league_map)

    if return_tournaments:
        return tournament_map


def setup():
    videos_map = {}
    tournament_map = _setup()

    for vod in lolesports.vods():
        tournament_id = lolesports.get_tournament_id(vod['reference'])
        tournament = tournament_map.get(tournament_id)
        if tournament is None:
            continue

        mapping = lolesports.get_mapping(tournament, vod['game'])
        youtube_id = lolesports.get_youtube_id(vod['source'])
        videos_map[youtube_id] = str(mapping)

    redis_db = datastore.get_redis_connection()
    redis_db.mset(videos_map)


if __name__ == "__main__":
    redis_db = datastore.get_redis_connection()
    if redis_db.get('setup_done') is None:
        setup()
        redis_db.set('setup_done', 'True')
