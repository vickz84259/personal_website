import os

from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session


def initialise():
    key = os.environ.get("TWITTER_KEY")
    secret = os.environ.get("TWITTER_SECRET")

    client = BackendApplicationClient(client_id=key)
    oauth = OAuth2Session(client=client)

    url = 'https://api.twitter.com/oauth2/token'
    token = oauth.fetch_token(
        token_url=url, client_id=key, client_secret=secret)

    return token
