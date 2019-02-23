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


def validate(youtube_url, reference):
    result = True
    try:
        lolesports.get_youtube_id(youtube_url)
        lolesports.get_tournament_id(reference)
    except (TypeError, AttributeError):
        result = False

    return result


def setup_tournaments():
    tournament_map = {}
    league_map = {}

    leagues = get_leagues()
    for league in leagues:
        tournaments = lolesports.get_tournaments(league['slug'])

        for tournament in tournaments:
            tournament_id = tournament['id']

            league_map[tournament_id] = tournament['leagueId']
            tournament_map[tournament_id] = tournament

    redis_db = datastore.get_redis_connection()
    redis_db.mset(league_map)

    return tournament_map


def setup():
    videos_map = {}
    tournament_map = setup_tournaments()

    vods = lolesports.get_vods()
    for vod in vods:
        youtube_url = vod['source']
        reference = vod['reference']
        if not validate(youtube_url, reference):
            continue

        tournament_id = lolesports.get_tournament_id(reference)
        tournament = tournament_map.get(tournament_id)
        if tournament is None:
            continue

        mapping = {}

        game_id = vod['game']
        mapping['game_id'] = game_id
        mapping['tournament_id'] = tournament_id

        for bracket in tournament['brackets'].values():
            for match in bracket['matches'].values():
                state = match.get('state', 'unresolved')
                if state == 'resolved':
                    for game in match['games'].values():
                        if game['id'] == game_id:
                            platform_id = game.get('platformId')
                            if platform_id is not None:
                                mapping['platform_id'] = game['platformId']
                                mapping['match_id'] = match['id']

                                youtube_id = lolesports.get_youtube_id(
                                    youtube_url)
                                videos_map[youtube_id] = str(mapping)

    redis_db = datastore.get_redis_connection()
    redis_db.mset(videos_map)


if __name__ == "__main__":
    redis_db = datastore.get_redis_connection()
    if redis_db.get('setup_done') is None:
        setup()
        redis_db.set('setup_done', 'True')
