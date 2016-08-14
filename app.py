# Standard modules

# Third-Party modules
import flask

# Project modules

app = flask.Flask(__name__)


@app.route('/')
def index():
    return flask.render_template('index.html')

if __name__ == '__main__':
    app.run()
