# Standard modules
import logging

# Third-Party modules
import flask

# Project modules
import twitter

logging.getLogger().setLevel(logging.INFO)

app = flask.Flask(__name__)


@app.route('/old')
def index():
    return flask.render_template('/old/index.html')


@app.route('/')
def home():
    return flask.redirect(flask.url_for('index'))


@app.route('/demo', methods=['POST', 'GET'])
def demo():
    tweets = []
    logging.info(flask.request.method)
    if flask.request.method == 'POST':
        keyword = flask.request.form['search_query']
        logging.info("keyword {}".format(keyword))
        tweets = twitter.search(keyword)

    return flask.render_template('demo/index.html', tweets=tweets)


if __name__ == '__main__':
    app.run()
