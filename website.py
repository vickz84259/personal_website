# Standard modules
import logging
import urllib.parse

# Third-Party modules
import flask
import requests

# Project modules
import riot
import datastore

logging.basicConfig(level=logging.INFO)

app = flask.Flask(__name__)


@app.route('/old')
def index():
    return flask.render_template('/old/index.html')


@app.route('/')
def home():
    return flask.redirect(flask.url_for('index'))


@app.route('/google8b87abaa24c74d5d.html')
def google_verification():
    return flask.render_template('google8b87abaa24c74d5d.html')


@app.route('/v1/summoner/<region>/<summoner_name>')
def get_summoner_details(region, summoner_name):
    summoner_name = urllib.parse.unquote(summoner_name)

    if (not riot.is_valid_region(region) or
            not riot.is_valid_summoner(summoner_name)):
        flask.abort(400)

    endpoint = f'/lol/summoner/v4/summoners/by-name/{summoner_name}'
    url = f'https://{riot.get_base_url(region)}{endpoint}'

    headers = riot.get_headers()
    summoner_details = requests.get(url, headers=headers).json()

    key = summoner_details['puuid']
    secrets = datastore.get_client_secrets(key)
    summoner_details['secrets'] = secrets

    return flask.jsonify(summoner_details)


if __name__ == '__main__':
    app.run()
