import flask
server = flask.Flask(__name__)

@server.route('/hola')
def index():
    return 'Hello Flask app'