import os
import requests
import logging

from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session


def get_token():
    """Gets the bearer token to be used to authenticate api requests

    Args:
        None

    Returns:
        A dict containing the token and its type. For example:
        {'token_type': 'bearer', 'access_token': 'dfaferqjkrqnrelkn'}
    """

    key = os.environ.get("TWITTER_KEY")
    secret = os.environ.get("TWITTER_SECRET")

    client = BackendApplicationClient(client_id=key)
    oauth = OAuth2Session(client=client)

    url = 'https://api.twitter.com/oauth2/token'
    token = oauth.fetch_token(
        token_url=url, client_id=key, client_secret=secret)

    return token


def get_tweets(query):
    url = 'https://api.twitter.com/1.1/search/tweets.json'
    params = {'q': query}

    token = get_token()['access_token']
    header_value = "Bearer {}".format(token)
    headers = {'Authorization': header_value}

    response = requests.get(url, params=params, headers=headers)
    decoded = response.json()
    logging.info(decoded)

    return decoded['statuses']


def get_oembed(tweet_id, username):
    api_url = 'https://publish.twitter.com/oembed'
    tweet_url = 'https://twitter.com/{}/statuses/{}'.format(username, tweet_id)

    params = {'url': tweet_url}
    response = requests.get(api_url, params=params)

    decoded = response.json()
    return decoded['html']


def search(query):
    tweets = get_tweets(query)
    result = []

    for tweet in tweets:
        tweet_id = tweet['id_str']
        username = tweet['user']['screen_name']

        oembed = get_oembed(tweet_id, username)
        result.append(oembed)

    logging.info(result)
    return result
