# Standard modules
import logging

# Third-Party modules
import flask

# Project modules
import twitter

logging.basicConfig(level=logging.INFO)

app = flask.Flask(__name__)


@app.route('/old')
def index():
    return flask.render_template('/old/index.html')


@app.route('/')
def home():
    return flask.redirect(flask.url_for('index'))


@app.route('/demo')
def demo():
    return twitter.initialise()


if __name__ == '__main__':
    app.run()
